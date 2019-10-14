using Discord;
using Discord.Commands;
using Discord.WebSocket;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Reflection;
using System.Threading.Tasks;
// IF IronPython BECOMES FEASIBLE:
//using IronPython.Hosting;
//using Microsoft.Scripting.Hosting;
//using System.Linq;

// Interpretation of User Input. User Input processed into Discord output through python/handler.py -> python/data.py -> python/handler.py -> CommandHandler.cs
// By LunaSeikaku

public class CommandHandler
{
    private CommandService ch_cmds;
    private DiscordSocketClient ch_client;
    private string PREFIX = System.IO.File.ReadAllText(System.IO.Path.GetDirectoryName(Assembly.GetEntryAssembly().Location) + @"\_prefix.txt");

    public async Task Send(SocketMessage s, string title, string description, string footer = "", string url = "", Dictionary<string,int> fields = null)
    {
        // Input context, title and description 
        // (footer, url, dict<string, int> 'fields' optional)
        // output an embed to context's channel with this data
        EmbedBuilder embd = new EmbedBuilder();

        if (fields != null)
        {
            foreach (var field in fields) { embd.AddField(field.Key, field.Value); }
        }

        embd.WithAuthor(s.Author)
            .WithColor(Color.Blue)
            //.WithCurrentTimestamp()
            //.WithTimestamp(time)

            .WithTitle(title)
            .WithDescription(description)
            .WithUrl(url)
            .WithFooter(footer);
            
        await s.Channel.SendMessageAsync("", false, embd.Build());
    }

    public async Task Install(DiscordSocketClient c)
    {
        ch_client = c;
        ch_cmds = new CommandService();

        await ch_cmds.AddModulesAsync(Assembly.GetEntryAssembly(), null); // load modular commands

        ch_client.MessageReceived += HandleCommand;
        ch_client.UserJoined += AnnounceUserJoined;
        ch_client.UserLeft += AnnounceUserLeft;
    }

    // If you want to add a Join message, do so below:
    public async Task AnnounceUserJoined(SocketGuildUser user)
    {
        await Task.Delay(0);
    }

    // If you want to add a Leave message, do so below:
    public async Task AnnounceUserLeft(SocketGuildUser user)
    {
        await Task.Delay(0);
    }

    public async Task HandleCommand(SocketMessage s)
    {
        var msg = s as SocketUserMessage;
        if (msg == null) return;

        var context = new SocketCommandContext(ch_client, msg);

        int argPos = 0;
        //string prefix = "!!";
        if (msg.HasStringPrefix(PREFIX, ref argPos))
        {
            // run command
            var result = await ch_cmds.ExecuteAsync(context, argPos, null);

            // if command unsuccessful, determine why and output message accordingly
            if (!result.IsSuccess)
            {
                switch (result.ToString())
                {
                    default:
                        await this.Send(s, "Sorry, an error occurred!", $"" + result.ToString());
                        break;

                    case "UnknownCommand: Unknown command.":
                        await msg.DeleteAsync();
                        await this.Send(s, "Sorry, command not found!",$"Use the command *{PREFIX}help* for a list of commands.");
                        break;
                }
            }
        }
    }

    // GENERIC COMMANDS BELOW:
    public class InfoModule : ModuleBase<SocketCommandContext>
    {
        [Command("help")]
        [Summary("Outputs a list of commands for this bot.")]
        [Alias("h")]
        public async Task HelpAsync()
        {
            string[] commands = new string[]
            {
              "*General Commands:*","help","speak","userinfo","\n",
              "*Math Commands:*","sum","power","root","\n",
              "*Touhou Commands:*","stages","battle","teambattle","balance","\n",
              "*Touhou Commands (player-related):*","catch","adventure","duel","teamduel","\n",
              "backpack","viewbackpack","secretary","setsecretary","setteam","clearteam","touhou"
            };
            await ReplyAsync(null, false, Send("List of Commands:", string.Join("\n", commands)));
        }

        [Command("speak")]
        [Summary("Echoes a message.")]
        [Alias("say","repeat")]
        public async Task speak(params string[] args)
        {
            await ReplyAsync(null, false, Send("", string.Join(" ", args))); // pretty nasty, but I don't see an alternative
        }

        [Command("userinfo")]
        [Summary("Returns info about the current user, or the user parameter, if one passed.")]
        [Alias("user", "whois")]
        public async Task UserInfoAsync([Summary("The (optional) user to get info from")]
        SocketUser user = null)
        {
            var userInfo = user ?? Context.Client.CurrentUser;
            await ReplyAsync(null, false, Send(userInfo.Username + "#" + userInfo.Discriminator, "",
                iurl: userInfo.GetAvatarUrl(),
                footer: "Date Joined: " + userInfo.CreatedAt.ToString().Substring(0, 10)
                ));
        }

        public Embed Send(string title, string description, string footer = "", string url = "", string iurl = "", string author = "", Dictionary<string, int> fields = null)
        {
            EmbedBuilder embd = new EmbedBuilder();

            if (fields != null)
            {
                foreach (var field in fields) { embd.AddField(field.Key, field.Value); }
            }

            embd.WithTitle(title)
                .WithDescription(description)

                .WithColor(Color.Blue)
                .WithUrl(url)
                .WithImageUrl(iurl)
                .WithFooter(footer)

                .WithAuthor(author);
            //.WithCurrentTimestamp()
            //.WithTimestamp(time)

            return embd.Build();
            //await s.Channel.SendMessageAsync("", false, embd.Build());
        }
    }

    // MATH COMMANDS BELOW:
    [Group("math")]
    public class MathModule : ModuleBase<SocketCommandContext>
    {
        /// Commands: ///
        [Command("sum")]
        [Summary("!!math sum 10 + 10 - 10 * 10 / 10 -> 10")]
        [Alias("total")]
        public async Task SumAsync(params string[] args)
        {
            string log = "";    // used in output
            int result = 0;     // current total of sum
            string m = "+";     // current modifier (+ - * /)
            bool first = true;  // true only on first iteration
            foreach (string s in args)
            {
                log += s;

                // first number in sum should be made into the starting result value:
                if (first) { int.TryParse(s, out result); first = false; }

                // if input is a modifier, set current modifier to it
                else if (s=="+"||s=="-"||s=="*"||s=="/") { m = s; }

                // If input is apparently a number beyond the first, attempt to calculate it with result: 
                else
                {
                    int i = 0;
                    int.TryParse(s, out i);
                    switch (m)
                    {
                        case "+":
                            result += i;
                            break;
                        case "-":
                            result -= i;
                            break;
                        case "*":
                            result *= i;
                            break;
                        default:
                            result /= i;
                            break;
                    }
                    // potential for more operations here!
                }
            }
            await ReplyAsync(null, false, Send(result.ToString(), "[" + log + "]"));
        }

        [Command("power")]
        [Summary("!!math power 2 3 -> 8")]
        public async Task PowerAsync( int num, int pow)
        {
             await ReplyAsync(null, false, Send(Math.Pow(num, pow).ToString(), "["+num.ToString()+"^"+pow.ToString()+"]"));
        }

        [Command("root")]
        [Summary("!!math root 8 3 -> 2")]
        public async Task RootAsync( int num, int root)
        {
            await ReplyAsync(null, false, Send(Math.Pow(num, 1.0/root).ToString(), "[" + num.ToString() + "√" + root.ToString() + "]"));
        }

        /// Methods: ///
        public Embed Send(string title, string description, string footer = "", string url = "", string iurl = "", string author = "", Dictionary<string, int> fields = null)
        {
            // Returns an Embed (by adding the inputs to an EmbedBuilder, then returning the built Embed):

            EmbedBuilder embd = new EmbedBuilder();

            if (fields != null)
            {
                foreach (var field in fields) { embd.AddField(field.Key, field.Value); }
            }

            embd.WithTitle(title)
                .WithDescription(description)

                .WithColor(Color.Blue)
                .WithUrl(url)
                .WithImageUrl(iurl)
                .WithFooter(footer)

                .WithAuthor(author);

            return embd.Build();
        }
    }

    // TOUHOU COMMANDS BELOW:
    [Group("2hu")]
    [Alias("touhou","th","t")]
    public class WarModule : ModuleBase<SocketCommandContext>
    {
        private bool initialised = false;
        //private dynamic dh; // currently don't need this to retain python info due to csv files
        private ProcessStartInfo psi = new ProcessStartInfo();
        private string root = System.IO.Path.GetDirectoryName(Assembly.GetEntryAssembly().Location);
        private string script = root + @"\python\handler.py";
        private string PATH = System.IO.File.ReadAllText(root + @"\_path.txt");

        // Declare process variable and arguments once (cannot outwith a method)
        public void Initialize()
        {
            // Process method
            // Create process info
            psi.FileName = PATH;

            // Process configuration
            psi.UseShellExecute = false;
            psi.CreateNoWindow = true;
            psi.RedirectStandardOutput = true;
            psi.RedirectStandardError = true;

            /* OLD: IronPython method (unfortunately doesn't like Pillow, numpy, matplotlib, etc as well as null inputs)
            // import python libraries for use after modulation into C#:
            ScriptEngine engine = Python.CreateEngine();
            var searchPaths = engine.GetSearchPaths();
            searchPaths.Add(root + @"\IronPythonStdLibraryIsUnfortunate");
            engine.SetSearchPaths(searchPaths);

            // IronPython initialisation for war commands:
            ScriptSource source = engine.CreateScriptSourceFromFile("data.py");
            ScriptScope scope = engine.CreateScope();
            source.Execute(scope);
            dynamic DataHandler = scope.GetVariable("Data");
            dh = DataHandler();

            // prevent recursion:*/
            initialised = true;
        }

        // Embed as variable that can be customized later (used in Task ParseAsync)
        public EmbedBuilder Hold(string title, string description, string footer = "", string url = "", string iurl = "", string author = "", Color? col = null, Dictionary<string, int> fields = null)
        {
            // return embd that can be edited before building and sending
            EmbedBuilder embd = new EmbedBuilder();

            if (fields != null)
            {
                foreach (var field in fields) { embd.AddField(field.Key, field.Value); }
            }

            embd.WithTitle(title)
                .WithDescription(description)

                .WithColor(col ?? Color.Red) // hack for optional parameter Color using null input if none defined in declaration
                .WithUrl(url)
                .WithImageUrl(iurl)
                .WithFooter(footer)

                .WithAuthor(author);

            return embd;
        }

        // Embed send immediately upon construction (streamlined)
        public Embed Send(string title, string description, string footer = "", string url = "", string iurl = "", string author = "", Color? col = null, Dictionary<string, int> fields = null)
        {
            // constructor for ready-to-use (built) embed
            EmbedBuilder embd = new EmbedBuilder();

            if (fields != null)
            {
                foreach (var field in fields) { embd.AddField(field.Key, field.Value); }
            }

            embd.WithTitle(title)
                .WithDescription(description)

                .WithColor(col ?? Color.Red)
                .WithUrl(url)
                .WithImageUrl(iurl)
                .WithFooter(footer)

                .WithAuthor(author);

            return embd.Build();
        }

        // Input string from data.py, output a (series of) Discord message(s)
        public async Task ParseAsync(string s)
        {
            // Convert non-parsed string from Data.py into discord embed(s)
            string[] li = s.Split(new[] { "***" }, StringSplitOptions.None);
            //li = li.Take(li.Count() - 1).ToArray();

            foreach (string l in li)
            {
                // error handling
                if (l != "")
                {
                    // First char is > for images only:
                    if (l[0] == '>')
                    {
                        var c = l.Split('>');
                        await Context.Channel.SendFileAsync(root + @"\chars\" + c[1] + @"\" + c[2] + ".png");
                    }

                    // Normal message:
                    else
                    {
                        var e = l.Split('|');
                        EmbedBuilder mbed = null; //= new EmbedBuilder();
                        for (int j = 0; j < e.Length-1; j++)
                        {
                            // Standard message(?):
                            if (e.Length == 1)
                            {
                                // if an Embed has been constructed and modified in the previous iteration, build and upload it to discord before creating a new one:
                                if (!(mbed is null)) { await ReplyAsync(null, false, mbed.Build()); }
                                mbed = Hold("",l,
                                        col: Color.Blue
                                        );
                                // send the Embed
                                await ReplyAsync(null, false, mbed.Build());
                                mbed = null;
                            }
                            // Nani?:
                            else if ((j*2)+1 >= e.Length)
                            {
                                if (!(mbed is null)) { await ReplyAsync(null, false, mbed.Build()); mbed = null; }
                            }
                            try
                            {
                                // Emoticon line for effect:
                                if (e[j*2][0]==':')
                                {
                                    if (!(mbed is null)) { await ReplyAsync(null, false, mbed.Build()); }
                                    await ReplyAsync(null, false, Send(e[j*2], e[(j*2)+1]));
                                    mbed = null;
                                }
                                // otherwise add fields to previous Embeds, including initiating Embed if it doesn't exist:
                                else
                                {
                                    if (mbed is null)
                                    {
                                        mbed = Hold(e[j*2],e[(j*2)+1],
                                                col: Color.Blue
                                                );
                                    }
                                    else
                                    {
                                        mbed.AddField(e[j*2],e[(j*2)+1]);
                                    }
                                }
                            } catch (Exception) {} // pass on exception
                        }
                    }
                }
            }
        }

        // Input user command, output it as argument into buffer.py->data.py, receive unparsed string to pass into Task ParseAsync 
        public async Task BattleFeed(string command, params string[] args)
        {
            // Parse command and its arguments into python, receive output from python and output to discord

            // initialize python class on first command runtime, but not anytime after
            if (!initialised) { Initialize(); }

            // retain any input arguments if applicable:
            var y; // recent C# updated forces me to declare this here and not as part of the line below
            y ?? args[0];
            var z;
            z ?? args[1];

            /* OLD: TEMPORARY SOLUTION FOR REMOVAL OF ?? FLAG:
            try { y = args[0]; }
            catch (Exception) {}
            try { z = args[1]; }
            catch (Exception) {}
            END OF TEMPORARY SOLUTION */

            // generate command line script, add it to the predefined ProcessStartInfo and write it to the CMD for logging:
            psi.Arguments = $"\"{script}\" {command} {y} {z}";
            Console.WriteLine(psi.Arguments);

            // run Python scripts and return it's unparsed string output:
            string s = "";
            string e = "";
            using (var process = Process.Start(psi))
            {
                s = process.StandardOutput.ReadToEnd();
                e = process.StandardError.ReadToEnd();
            }

            Console.WriteLine("-");
            Console.WriteLine(s);
            Console.WriteLine(e);
            Console.WriteLine("-");

            // pass the unparsed string into the parser, which also posts it to Discord:
            /* OLD: IronPython method:
            string s = dh.commands["battle"](blueCorner, redCorner);*/
            await ParseAsync(s);
        }

        //////////////////////////////
        // GENERAL TOUHOU COMMANDS: //
        // ~war battle Reimu Marisa //
        [Command("singlebattle")]
        [Summary("Witness 2 named Touhous fight to the death for your enjoyment.")]
        [Alias("battle","bat","b")]
        public async Task SinglebattleAsync(string blueCorner = "", string redCorner = "")
        {
            await BattleFeed("battle", blueCorner, redCorner);
        }

        // ~war teambattle MyTeam YourTeam (6v6 is temporary, can involve XvX Touhou fighting against each other)
        [Command("teambattle")]
        [Summary("Witness 2 Touhou teams fight to the death for your enjoyment.")]
        [Alias("multibattle", "multiplayer")]
        public async Task TeambattleAsync(string a = "", string b = "", string c = "", string d = "", string e = "", string f = "",
                                          string u = "", string v = "", string w = "", string x = "", string y = "", string z = "")
        {
            await BattleFeed("teambattle", a,b,c,d,e,f, u,v,w,x,y,z);
        }
        
        // ~war multiteam Opponent'sDiscordMention (takes in your details too automatically)
        [Command("multiteam")]
        [Summary("Witness 2 of your Touhou teams fight to the death for your enjoyment.")]
        public async Task MultiteamAsync(SocketUser opponent = null)
        {
            var myInfo = Context.Client.CurrentUser;
            var opponentInfo = opponent ?? Context.Client.CurrentUser;
            await BattleFeed("multiteam", myInfo.Username + "#" + myInfo.Discriminator, opponentInfo.Username + "#" + opponentInfo.Discriminator);
        }

        // ~war stages TheChosenTouhou
        [Command("stages")]
        [Summary("Witness a Touhou attempt to fight through 6 stages of Touhou characters for your enjoyment!")]
        [Alias("stage", "levels", "level")]
        public async Task StagesAsync(string protagonist = "")
        {
            await BattleFeed("stages", protagonist);
        }

        // ~war balance Me You
        [Command("balance")]
        [Summary("Have 2 Touhou's fight each other 10 times, then graph their results to attempt to balance them.")]
        [Alias("b", "bal")]
        public async Task BalanceAsync(string blueCorner = "", string redCorner = "")
        {
            await BattleFeed("balance", blueCorner, redCorner);
        }

        ////////////////////////////////////
        // DISCORD USER SPECIFIC COMMANDS: //
        // ~war catch                     //
        [Command("catch")]
        [Summary("Gacha mode.")]
        [Alias("gacha","roll", "rng")]
        public async Task CatchAsync()
        {
            //var myInfo = Context.Client.CurrentUser; // that's this bot!
            var myInfo = Context.Message.Author; // the user who typed the command that this bot is processing
            await BattleFeed("catch", myInfo.Id + "#" + myInfo.Username);
        }

        [Command("adventure")]
        [Summary("Stages command but with Player's own Touhou.")]
        [Alias("adv")]
        public async Task AdventureAsync(string theChosenOne = "")
        {
            var myInfo = Context.Message.Author;
            await BattleFeed("adventure", myInfo.Id + "#" + myInfo.Username, theChosenOne);
        }

        [Command("duel")]
        [Summary("1v1 with Player's own Secretary versus Opponent's Secretary.")]
        [Alias("d")]
        public async Task DuelAsync(SocketUser opponent = null)
        {
            var myInfo = Context.Message.Author;
            var opponentInfo = opponent ?? Context.Client.CurrentUser; // bot opponent if no opponent selected
            await BattleFeed("duel", myInfo.Id + "#" + myInfo.Username, opponentInfo.Id + "#" + opponentInfo.Username);
        }

        [Command("teamduel")]
        [Summary("6v6 with Player's own Team versus Opponent's Team.")]
        [Alias("d")]
        public async Task TeamDuelAsync(SocketUser opponent = null)
        {
            var myInfo = Context.Message.Author;
            var opponentInfo = opponent ?? Context.Client.CurrentUser;
            await BattleFeed("teamduel", myInfo.Id + "#" + myInfo.Username, opponentInfo.Id + "#" + opponentInfo.Username);
        }

        // ~war s
        [Command("secretary")]
        [Summary("Shows user's secretary and commands to interact with them.")]
        [Alias("s")]
        public async Task SecretaryAsync()
        {
            var myInfo = Context.Message.Author;
            await BattleFeed("secretary", myInfo.Id + "#" + myInfo.Username);
        }

        // ~war ss
        [Command("setsecretary")]
        [Summary("Changes user's secretary to one from their Backpack if possible.")]
        [Alias("ss")]
        public async Task SetSecretaryAsync(string theChosenOne = "")
        {
            var myInfo = Context.Message.Author;
            await BattleFeed("setsecretary", myInfo.Id + "#" + myInfo.Username,theChosenOne);
        }

        // ~war t
        [Command("team")]
        [Summary("Shows user's team and commands to interact with them.")]
        [Alias("t")]
        public async Task TeamAsync()
        {
            var myInfo = Context.Message.Author;
            await BattleFeed("team", myInfo.Id + "#" + myInfo.Username);
        }

        // ~war st
        [Command("setteam")]
        [Summary("Changes user's team to Touhou from their Backpack if possible.")]
        [Alias("st")]
        public async Task SetTeamAsync(string a = "", string b = "", string c = "", string d = "", string e = "", string f = "")
        {
            var myInfo = Context.Message.Author;
            await BattleFeed("team", myInfo.Id + "#" + myInfo.Username,a,b,c,d,e,f);
        }

        // ~war ct
        [Command("clearteam")]
        [Summary("Clear user's team, putting them into their Backpack.")]
        [Alias("ct")]
        public async Task ClearTeamAsync(string a = "", string b = "", string c = "", string d = "", string e = "", string f = "")
        {
            var myInfo = Context.Message.Author;
            await BattleFeed("clearteam", myInfo.Id + "#" + myInfo.Username, a, b, c, d, e, f);
        }

        // ~war bp
        [Command("backpack")]
        [Summary("Shows user's backpack and commands to interact with backpack.")]
        [Alias("bp")]
        public async Task BackpackAsync()
        {
            var myInfo = Context.Message.Author;
            await BattleFeed("backpack", myInfo.Id + "#" + myInfo.Username);
        }
        // ~war vp
        [Command("viewbackpack")]
        [Summary("Shows user's backpack.")]
        [Alias("vp")]
        public async Task ViewBackpackAsync()
        {
            var myInfo = Context.Message.Author;
            await BattleFeed("viewbackpack", myInfo.Id + "#" + myInfo.Username);
        }

        // ~war 2
        [Command("touhou")]
        [Summary("Shows a Touhou's stats.")]
        [Alias("2")]
        public async Task TouhouAsync(string touhouname)
        {
            await BattleFeed("touhou", touhouname);
        }

        // MORE COMMANDS TO BE ADDED HERE
    }
}