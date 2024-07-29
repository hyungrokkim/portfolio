class Numeric
    def yotta; self*1e24; end
    def zetta; self*1e21; end
    def exa; self*1e18; end
    def peta; self*1e15; end
    def tera; self*1e12; end
    def giga; self*1e9; end
    def mega; self*1e6; end
    def kilo; self*1e3; end
    def hecto; self*1e2; end
    def deca; self*10; end
    def deci; self*1e-1; end
    def centi; self*1e-2; end
    def milli; self*1e-3; end
    def micro; self*1e-6; end
    def nano; self*1e-9; end
    def pico; self*1e-12; end
    def femto; self*1e-15; end
    def atto; self*1e-18; end
    def zepto; self*1e-21; end
    def yocto; self*1e-24; end
    def dimension
        []
    end
    def dimension=(a)
        Dimensional.new(self,a)
    end
    def value
        self
    end
end
require 'forwardable'
class Dimensional < Numeric
    extend Forwardable
    attr_accessor :value
    attr_writer :dimensions
    protected :"dimensions="
    def initialize(value,dimensions=[])
        raise ArgumentError if dimensions.size != 7
        @value, @dimensions=value, dimensions
        @value.methods.each {|m| def_delegator(:@value,m.intern)}
    end
    def +(a)
        raise ArgumentError unless dimensions==a.dimensions
        Dimensional.new(value+a.value, dimensions.clone)
    end
    def -(a)
        raise ArgumentError unless dimensions==a.dimensions
        Dimensional.new(value-a.value, dimensions.clone)
    end
    def *(a)
        Dimensional.new(value*a.value, dimensions.zip(a.dimensions).map {|i| i[0]+i[1]})
    end
    def /(a)
        Dimensional.new(value/a.value, dimensions.zip(a.dimensions).map {|i| i[0]-i[1]})
    end
    def **(a)
        raise ArgumentError if a.dimension!=[]
        Dimensional.new(value**a.value, dimensions.map {|i| i*a})
    end
    def div(a)
        div=self/a
        div.value=div.value.to_i
        div
    end
    def divmod(a)
        divmod=value.divmod(a.value)
        divmod[0].dimension=dimension
        divmod
    end
    def %(a)
        Dimensional.new(value%a.value, dimensions.zip(a.dimensions).map {|i| i[0]-i[1]})
    end
    def quo(a)
        Dimensional.new(value.quo a.value, dimensions.zip(a.dimensions).map {|i| i[0]-i[1]})
    end
    def remainder(a)
        Dimensional.new(value.remainder a.value, dimensions.zip(a.dimensions).map {|i| i[0]-i[1]})
    end
    def @-(a)
        Dimensional.new(-value, dimensions.clone)
    end
    def <=>(a)
        raise ArgumentError unless dimensions==a.dimensions
        value<=>a.value
    end
    private
    def multiplicative_operator(a,m=:-)
        define_method a do |b|
            Dimensional.new(value.send(a, b.value), dimensions.zip(b.dimensions).map {|i| i[0].send m, i[1]}
        end
    end
end
