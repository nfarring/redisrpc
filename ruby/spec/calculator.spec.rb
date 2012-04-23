require File.expand_path( '../spec_helper.rb', __FILE__ )
require File.expand_path( '../../examples/calc.rb', __FILE__ )

describe Calculator do
  [true,false].each do |over_redisrpc|
    context "when run ( over_redisrpc ? 'over redisrpc' : 'locally')" do

      if( over_redisrpc )
        before(:each) do 
          @server_pid = fork{ RedisRPC::Server.new( Redis.new($REDIS_CONFIG), 'calc', Calculator.new ).run! }
        end
        after(:each){ Process.kill 9, @server_pid }
        let(:calculator){ RedisRPC::Client.new( $REDIS,'calc', 1) }
      else
        let(:calculator){ Calculator.new }
      end

      it 'should calculate' do
        calculator.val.should == 0.0
        calculator.add(3).should == 3.0
        calculator.sub(2).should == 1.0
        calculator.mul(14).should == 14.0
        calculator.div(7).should == 2.0
        calculator.val.should == 2.0
        calculator.clr.should == 0.0
        calculator.val.should == 0.0
      end

      it 'should raise when missing method is called' do
        expect{ calculator.some_missing_method }.to raise_error
      end
    end
  end
end
