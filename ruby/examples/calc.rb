class Calculator
    # A simple, mutable calculator used for testing.
    # referenced explicitly in ../spec/calculator.spec.rb
    
    def initialize
        @acc = 0.0
    end

    def clr
        @acc = 0.0
    end

    def add(number)
        @acc += number
    end

    def div(number)
        @acc /= number
    end

    def mul(number)
        @acc *= number
    end

    def sub(number)
        @acc -= number
    end

    def val
        return @acc
    end
end
