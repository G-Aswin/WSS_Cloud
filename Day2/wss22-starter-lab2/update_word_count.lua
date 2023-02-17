#!lua name=update_word_count
local function update_word_count(keys, args)
    local countername = keys[1]
    local member = keys[2]
    local stream = keys[3]
    local group = keys[4]
    local value = tonumber(args[1])
    local fileid = args[2]

    

    -- Increment count of a word from a file
    -- First ack and check return value
    -- Also get all the words in once in lua and loop it out

    redis.call('XACK', stream, group, fileid)
    redis.call('ZINCRBY', countername, value, member)

    return 'ok'
end
redis.register_function('update_word_count', update_word_count)
