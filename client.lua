local plrs = game.Players
local fns = {}
local amountchatted = 0
local cooldown = false
local url = "[webhook url here]"
local req = request or syn.request
local musiclist = {}
local voicebubble = game:GetService("CoreGui").BubbleChat["BubbleChat_"..game.Players.LocalPlayer.UserId].VoiceBubble.RoundedFrame.Contents.Insert
print("boutta load")


local listmsg = "Commands: !list - lists commands;  !play [SONG NAME] - queues and plays songs; !voteskip - to be added"
function Queuechat(msg,towhom)
    repeat
        wait()
    until not cooldown
   game.ReplicatedStorage.DefaultChatSystemChatEvents.SayMessageRequest:FireServer(msg,towhom)
   amountchatted = amountchatted + 1
   if amountchatted == 3 then
    amountchatted = 0
    cooldown = true
    wait(3)
    cooldown = false
   end
end
function Chatted(plr,msg)
    if string.sub(msg,1,1) == "!" then
        for i,v in pairs(fns) do
            print(string.sub(msg,2,5))
            if string.sub(msg,2,5) == i then
                print("detected")
                v(plr,string.sub(msg,7,#msg))
            end
        end
    end
end

function PlrAdded(plr)
    plr.Chatted:Connect(function(msg)
        Chatted(plr,msg)
    end)
end

function MainReq(song)
    req{
        Url = url,
        Method = 'POST', 
        Body = "{\"content\":\"!yt \\\""..song.."\\\"\"}",
        Headers = {
        ['Content-Type'] = 'application/json'
        }
        }
end
function PlayReq(song)
    req{
        Url = url,
        Method = 'POST', 
        Body = "{\"content\":\"!start \\\""..song.."\\\"\"}",
        Headers = {
        ['Content-Type'] = 'application/json'
        }
        }
end
function fns.list(plr,msg)
    Queuechat("/w "..plr.Name,"All")
    Queuechat(listmsg,"To "..plr.Name)
end
function fns.play(plr,msg)
    Queuechat("/w "..plr.Name,"All")
    Queuechat("Please wait, your song is being added to the queue.","To "..plr.Name)
    table.insert(musiclist,msg)
    MainReq(msg)
end


for i,plr in pairs(plrs:GetChildren()) do
    PlrAdded(plr)

end
game.Players.PlayerAdded:Connect(PlrAdded)
print("loaded")
while wait(5) do
    print("check")
    if #musiclist ~= 0 then
    print("waiting")
    if voicebubble.Image == "rbxasset://textures/ui/VoiceChat/MicDark/Unmuted0.png" then
    print("check 2")
    wait(5)
    if voicebubble.Image == "rbxasset://textures/ui/VoiceChat/MicDark/Unmuted0.png" then
       PlayReq(musiclist[1])
       print("yeah the song is done loading, playing next")
        Queuechat("Now Playing: "..musiclist[1],"To "..plr.Name)
       table.remove(musiclist,1)
    end
end
end
