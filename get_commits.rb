require 'open-uri'
require 'zlib'
require 'yajl'
require 'pp'
require 'json'

curses = ["fuck", 
    "bitch",
    "stupid", 
    " tits", 
    "asshole", 
    "cocksucker", 
    "cunt", 
    " hell ", 
    "douche", 
    "testicle", 
    "twat", 
    "bastard", 
    "sperm", 
    "shit", 
    "dildo", 
    "wanker", 
    "prick", 
    "penis", 
    "vagina", 
    "whore",
]
d = Date.today.prev_day.to_s
hour = Time.new.hour.to_s
d = d + '-' + hour
url = 'http://data.githubarchive.org/' + d + '.json.gz'
gz = open(url)
js = Zlib::GzipReader.new(gz).read
a = Array.new 
Yajl::Parser.parse(js) do |event|
    begin
        message = event['payload']['shas'][0][2]
        output = Hash.new
        curses.each do |curse|
            if message.include? curse
                output['created_at'] = event['repository']['created_at']
                output['message'] = event['payload']['shas'][0][2]
                output['commiter'] = event['payload']['shas'][0][3]
                output['commiturl'] = event['url']
                output['userurl'] = "github.com/" + event['actor']
                a.push(output)
                next
            end
        end
    rescue
    end
end
puts JSON.dump(a)
