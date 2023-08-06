using Pkg


# Import IAI
if isdefined(Main, :IAISysImg) && isdefined(IAISysImg, :__init__)
  iai_version = IAISysImg.VERSION
  # Run delayed IAISysImg init
  IAISysImg.__init__()
else
  iai_version = if VERSION < v"1.4"
    get(Pkg.installed(), "IAI", nothing)
  else
    pkg = [v for (k, v) in Pkg.dependencies() if v.name == "IAI"]
    length(pkg) > 0 ? pkg[1].version : nothing
  end
  if iai_version == nothing
    error("IAI is not present in your Julia installation. Please follow the " *
          "instructions at " *
          "https://docs.interpretable.ai/stable/IAI-Python/installation")
  end
  @eval Main import IAI
end
@assert isdefined(Main, :IAI)


# Check that a compatible version of IAI.jl is present
const REQUIRED_IAI_VERSION = v"1.0.0"

if Base.thispatch(iai_version) < Base.thispatch(REQUIRED_IAI_VERSION)
  error("This version of the `interpretableai` Python package requires IAI " *
        "version $(Base.thispatch(REQUIRED_IAI_VERSION)). Version " *
        "$iai_version of IAI modules is installed. Please upgrade your IAI " *
        "installation or downgrade to an older version of the " *
        "`interpretableai` Python package.")
end


# Make sure other dependencies are present
for package in ("PyCall", "DataFrames", "CategoricalArrays")
  is_installed = if VERSION < v"1.4"
    haskey(Pkg.installed(), package)
  else
    any(v -> v.name == package && v.is_direct_dep, values(Pkg.dependencies()))
  end
  is_installed || Pkg.add(package)
end


# Add extra helpers for py<-->jl conversions
include("convert.jl")


# Add julia methods for output
@eval IAI begin
  function to_html(obj)
    if showable("text/html", obj)
      io = IOBuffer()
      show(io, MIME("text/html"), obj)
      String(take!(io))
    else
      return nothing
    end
  end
  function to_json(obj)
    io = IOBuffer()
    try
      write_json(io, obj; indent=nothing)
    catch TypeError
      write_json(io, obj)
    end
    String(take!(io))
  end
  function from_json(str)
    io = IOBuffer(str)
    read_json(io)
  end
end
