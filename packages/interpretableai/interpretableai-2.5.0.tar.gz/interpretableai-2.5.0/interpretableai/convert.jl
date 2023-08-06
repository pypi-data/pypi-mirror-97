module IAIConvert
  using CategoricalArrays
  using DataFrames
  using PyCall
  using Main.IAI

  const pd = pyimport("pandas")
  const np = pyimport("numpy")
  const iai = pyimport("interpretableai.iai")


  const DTYPE_MAPPING = Dict(
    "float64" => Float64,
    "int64" => Int,
    "bool" => Bool,
  )


  function convert_to_jl_dataframe(df::PyObject; normalizenames::Bool=true)
    pyisinstance(df, pd.DataFrame) || error("df is not a pandas data frame")

    vnames = Symbol.(df)
    if normalizenames
      vnames = [Symbol(replace(string(v), '.' => '_')) for v in vnames]
    end

    cols = []
    for (_, col) in df.items()
      push!(cols, convert_to_jl(col))
    end
    DataFrame(cols, vnames)
  end

  function convert_to_jl_series(series::PyObject)
    pyisinstance(series, pd.Series) || error("series is not a pandas series")

    vals = collect(series)
    missing_inds = findall(x -> x isa Number && isnan(x), vals)
    vals[missing_inds] .= missing

    dtype = series.dtype
    if pyisinstance(series.array, iai.MixedData)
      ordinal_levels = series.array._ordinal_levels
      if ordinal_levels != nothing
        vals = IAI.make_mixed_data(vals, collect(ordinal_levels))
      else
        vals = IAI.make_mixed_data(vals)
      end

    elseif pyisinstance(dtype, pd.CategoricalDtype)
      levels = collect(dtype.categories)
      ordered = dtype.ordered

      vals = CategoricalArray(vals, ordered=ordered)
      levels!(vals, levels)
    elseif dtype.name in keys(DTYPE_MAPPING)
      vtype = DTYPE_MAPPING[dtype.name]
      if !isempty(missing_inds)
        vtype = Union{vtype,Missing}
      end
      vals = Vector{vtype}(vals)
    end

    vals
  end

  function convert_to_jl_ndarray(o::PyObject)
    if length(o.shape) == 1
      collect(o)
    elseif length(o.shape) == 2
      vcat(reshape.(collect.(o), Ref((1, o.shape[2])))...)
    end
  end


  convert_to_jl(o) = o
  function convert_to_jl(o::PyObject)
    if pyisinstance(o, pd.Series)
      convert_to_jl_series(o)
    elseif pyisinstance(o, pd.DataFrame)
      convert_to_jl_dataframe(o)
    elseif pyisinstance(o, np.ndarray)
      convert_to_jl_ndarray(o)
    else
      o
    end
  end
  function convert_to_jl(o::Array{PyObject})
    convert.(String, o)
  end

  function convert_to_jl(p::Pair)
    convert_to_jl(p.first) => convert_to_jl(p.second)
  end
  function convert_to_jl(pairs::Base.Iterators.Pairs)
    Pair[convert_to_jl(p) for p in pairs]
  end
  function convert_to_jl(o::Tuple)
    Tuple([convert_to_jl(o_i) for o_i in o])
  end

  # For multi-vis, convert from Python 2-tuple (string, list of tuples) to
  # Julia Pair of String=>Vector{Pair}
  convert_to_jl_pairs(o) = o
  convert_to_jl_pairs(o::PyObject) = o._jl_obj
  convert_to_jl_pairs(o::Array) = convert_to_jl_pairs.(o)
  function convert_to_jl_pairs(o::Tuple)
    if length(o) == 2
      Pair(convert_to_jl_pairs(o[1]), convert_to_jl_pairs(o[2]))
    else
      error("Should only be converting a 2-element tuple to pairs")
    end
  end


  convert_to_py(o) = o
  convert_to_py(o::Tuple) = convert_to_py.(o)
  convert_to_py(o::Dict) = Dict(k => convert_to_py(v) for (k, v) in o)

  function convert_to_py(o::AbstractDataFrame)
    # Can't use pd.DataFrame(dict) to create because it doesn't preserve order
    cols = [convert_to_py(col) for col in eachcol(o)]
    df = pd.concat(pd.Series.(cols), axis=1)
    df.columns = names(o)
    df
  end
  function convert_to_py(o::DataFrameRow)
    # Convert to pd.DataFrame first, and then get first row from iterator
    df = convert_to_py(DataFrame(o))
    first(df.iterrows())[2]
  end

  function convert_to_py(o::AbstractCategoricalVector)
    function get_value(v)
      # If DataAPI.unwrap is defined, try to use it to unwrap the value to a
      # non-categorical value
      @static if isdefined(CategoricalArrays, :DataAPI) &&
                 isdefined(CategoricalArrays.DataAPI, :unwrap)
        new_v = CategoricalArrays.DataAPI.unwrap(v)
        if !(new_v isa CategoricalArrays.CategoricalValue)
          return new_v
        end
      end
      # Otherwise fallback to Base.get
      get(v)
    end

    col = Any[ismissing(x) ? x : get_value(x) for x in o]
    dtype = pd.CategoricalDtype(categories=levels(o), ordered=isordered(o))
    pd.Series(convert_to_py(col), dtype=dtype)
  end
  function convert_to_py(o::AbstractVector)
    if nonmissingtype(eltype(o)) <: IAI.IAIBase.MixedDatum
      vals = convert_to_py(Vector{Any}(IAI.undo_mixed_data(o)))
      iai.MixedData(vals, ordinal_levels=IAI.IAIBase.levels_ordinal(o))
    else
      missing_inds = findall(ismissing, o)
      if !isempty(missing_inds)
        o[missing_inds] .= NaN
      end
      o
    end
  end
  function convert_to_py(o::SubArray)
    convert_to_py(getindex(parent(o), o.indices...))
  end
end


# Wrap all exported functions with py<->julia conversion
for f in names(IAI)
  getfield(IAI, f) isa Module && continue

  f_mod = Symbol(replace(String(f), "!" => ""), "_convert")
  # Define new function in IAI to extend
  @eval IAI function $f_mod end
  # Define wrapper for IAI function to convert all PyObject
  @eval Main begin
    function (IAI.$f_mod)(args...; kwargs...)
      out = (IAI.$f)(IAIConvert.convert_to_jl.(args)...;
                     IAIConvert.convert_to_jl(kwargs)...)
      IAIConvert.convert_to_py(out)
    end
  end

end

@eval Main begin
  if isdefined(IAI, :MultiTreePlot_convert)
    function IAI.MultiTreePlot_convert(tuple::Tuple)
      IAI.MultiTreePlot_convert(IAIConvert.convert_to_jl_pairs(tuple))
    end
  end
  if isdefined(IAI, :MultiQuestionnaire_convert)
    function IAI.MultiQuestionnaire_convert(tuple::Tuple)
      IAI.MultiQuestionnaire_convert(IAIConvert.convert_to_jl_pairs(tuple))
    end
  end
end
