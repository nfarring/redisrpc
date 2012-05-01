require 'bundler'
begin
  Bundler.require(:default,:development)
rescue Bundler::BundlerError => e
  $stderr.puts e.message
  $stderr.puts "Run `bundle install` to install missing gems"
  exit e.status_code
end

def MultiJson.default_adapter
  :ok_json
end


RSpec.configure do |config|
  config.before :suite do
    raise 'redis-server must be on your path to run this test' if `which redis-server`.empty?
    $REDIS_CONF_PATH = File.expand_path('../redis-test.conf',__FILE__)

    redis_conf_contents = File.read($REDIS_CONF_PATH)
    raise "pidfile must be specified in #{$REDIS_CONF_PATH}" unless redis_conf_contents['pidfile'] 

    $REDIS_CONFIG = {
      :host => 'localhost', 
      :port => (redis_conf_contents.match(/port ([0-9]+)/)[1].to_i rescue 6379), 
      :db   => 15 # we'll be flushing regularly; db 15 is traditionally reserved for test
      }

    $stdout.write "Starting Redis on port #{$REDIS_CONFIG[:port]}... "; $stdout.flush
    `redis-server #{$REDIS_CONF_PATH}`
    puts 'Done.'
    
    $REDIS = Redis.new($REDIS_CONFIG)
    begin
      $REDIS.ping
    rescue Timeout::Error, Errno::ECONNREFUSED
      retries ||= 3
      sleep 1 and retry unless (retries-=1).zero?
      $stderr.puts 'Could not connect to Redis after 3 tries.'
      exit
    end
  end

  config.around :each do |example|
    $REDIS.flushdb
    example.call
  end

  config.after :suite do
    pidfile = (File.read($REDIS_CONF_PATH).match(/pidfile (.+)$/)[1].chomp rescue nil)
    $stdout.write "\nKilling test redis server... "; $stdout.flush
    Process.kill("KILL", File.read(pidfile).chomp.to_i )
    File.unlink(pidfile)
    puts 'Done.'
  end
end
