redisrpc: leightweight RPC for Redis

---

This example Python code shows a client accessing a Calculator instance remotely.

calc.py

    class Calculator(object):
        """A simple calculator class with state used for testing."""

        def __init__(self):
            self.acc = 0.0

        def __str__(self):
            return '%s' % self.acc
        
        def clr(self):
            self.acc = 0.0

        def add(self,number):
            self.acc += number
            return self.acc

        def div(self,number):
            self.acc /= number
            return self.acc

        def mul(self,number):
            self.acc *= number
            return self.acc

        def sub(self,number):
            self.acc -= number
            return self.acc

        def val(self):
            return self.acc


server.py

    import redis

    from redisrpc import RedisRPCServer
    from calc import Calculator

    redis_server = redis.Redis()
    server = RedisRPCServer(redis_server, 'calc', Calculator())
    server.run()


client.py

    import traceback

    import redis

    from redisrpc import RedisRPCClient
    from calc import Calculator

    def do_calculations(calculator):
        calculator.clr()
        print(calculator.add(2.0))
        print(calculator.add(5.5))
        print(calculator.sub(3.1))
        print(calculator.mul(2))
        print(calculator.div(3))
        try:
            print(calculator.foo())
        except:
            traceback.print_exc()
        calculator.clr()

    # Local object.
    calculator = Calculator()
    do_calculations(calculator)

    redis_server = redis.Redis()

    # Remote object.
    calculator = RedisRPCClient(redis_server, 'calc')
    do_calculations(calculator)

    # Remote object with local run-time type checking.
    calculator = RedisRPCClient(redis_server, 'calc', Calculator)
    do_calculations(calculator)

