using Discord.WebSocket;
using System;
using System.Reflection;
using System.Threading.Tasks;

// The hosted Discord Bot task.
// By LunaSeikaku
// simply converts C# output into Python input, and Python output into C# input

namespace Seigabot
{
    class Program
    {
        public DiscordSocketClient Client;
        public CommandHandler Handler;
        private string TOKEN = System.IO.File.ReadAllText(System.IO.Path.GetDirectoryName(Assembly.GetEntryAssembly().Location) + @"\_token.txt"); // Discord Bot Token
        static void Main(string[] args) => new Program().Start().GetAwaiter().GetResult();

        public async Task Start()
        {
            Client = new DiscordSocketClient();

            Handler = new CommandHandler(); // CommandHandler.cs

            await Client.LoginAsync(Discord.TokenType.Bot,TOKEN);

            await Client.StartAsync();

            await Handler.Install(Client);

            Client.Ready += Client_Ready;

            await Task.Delay(-1);
        }

        private async Task Client_Ready()
        {
            Console.WriteLine("SEIGA online.");
            return;
        }
    }
}
