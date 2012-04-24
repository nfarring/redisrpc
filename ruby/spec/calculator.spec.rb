require File.expand_path( '../spec_helper.rb', __FILE__ )
require File.expand_path( '../../examples/calc.rb', __FILE__ )

describe Calculator do
  [true,false].each do |over_redisrpc|
    context "when run #{( over_redisrpc ? 'over redisrpc' : 'locally')}" do

      if( over_redisrpc )
        let(:rpc_server_builder){ lambda{ RedisRPC::Server.new( Redis.new($REDIS_CONFIG), 'calc', Calculator.new ) } }
        before(:each) do 
          @server_pid = fork{ rpc_server_builder.call.run }
        end
        after(:each){ Process.kill(9, @server_pid); rpc_server_builder.call.flush_queue! }
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
        expect{ calculator.a_missing_method }.to raise_error(
          over_redisrpc ? RedisRPC::RemoteException : NoMethodError
        )
      end

      it 'should raise timeout when execution expires' do
        expect{ calculator.send(:sleep,2) }.to raise_error RedisRPC::TimeoutException
      end if over_redisrpc
    end
  end
end
