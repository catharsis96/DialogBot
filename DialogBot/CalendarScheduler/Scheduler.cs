using Microsoft.Bot.Builder.Dialogs;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Web;
using System.Threading.Tasks;
using Microsoft.Bot.Connector;
using System.Text.RegularExpressions;

namespace DialogBot.CalendarScheduler
{
    [Serializable]
    public class Scheduler : IDialog<EventDate>
    {

        public static void FileWrite()
        {
            string targetDir = string.Format(@"C:\Users\mami\Documents");

            var processInfo = new System.Diagnostics.ProcessStartInfo("cmd.exe", "/c " + @"python script.py");
            processInfo.WorkingDirectory = targetDir;
            //Console.ReadKey();
            var process = System.Diagnostics.Process.Start(processInfo);
            process.WaitForExit();

            //Console.ReadKey();
        }

        public static string GetFromFile()
        {
            FileWrite();
            string text = System.IO.File.ReadAllText(@"C:\Users\mami\Documents\exicute.txt");

            //string[] lines = System.IO.File.ReadAllLines(@"C:\Users\mami\Documents\exicute.txt");

            // Display the file contents by using a foreach loop.
            /*string text = "";
            foreach (string line in lines)
            {
                // Use a tab to indent each line of the file.
                text = (text + "\n" + lines);
            }*/

            // Display the file contents by using a foreach loop.

            return text;
        }

        EventDate date;
        public async Task StartAsync(IDialogContext context)
        {
            if (date == null) date = new EventDate();
            context.Wait(MessageReceivedAsync);

        }

        private async Task MessageReceivedAsync(IDialogContext context, IAwaitable<IMessageActivity> result)
        {
            var message = await result;
            var repl =await Reply(message.Text);
            await context.PostAsync(repl);
            context.Wait(MessageReceivedAsync);
        }

        private async Task<string> Reply(string text)
        {
            
            if (text.Contains("help"))
            {
                return @"This is a simple vk event bot.
Example of commands include:
  event today
  event tomorrow
  do i have smth at 10.09.2016
Your date input must be in format dd.mm.yyyy";
            }
            if (text.Contains("hi") || text.Contains("hello"))
                return "Hello! I am an Vkontakte Notify Bot.I can tell you about interesting events in social network";
            if (text.Contains("bye"))
                return "Good bye! Have a good day!";
            if (text.Contains("who are you"))
                return
                    "I am an Vkontakte Notify Bot. If you want to know about any of interesting events in social network, you can ask me about it";
            if (text.Contains("develop") || text.Contains("create") || text.Contains("invent"))
                return "I was developed by MSP on the MSP Summit 2016";
            if (text.Contains("event") && text.Contains("today"))
                return await date.BuildResult(Dates.Today);
            if (text.Contains("hat's up"))
                return GetFromFile();
            if (text.Contains("event") && text.Contains("tomorrow"))
                return await date.BuildResult(Dates.Tomorrow);
            if (text.Contains("remind me about"))
                return date.AddDate(text.Replace("remind me about","").Replace("at",""));
            CultureInfo culture=new CultureInfo("ru-RU");
            var match = Regex.Match(text,"[0-9]{1,2}.{1}[0-9]{1,2}.20[0-9]{2}");
            if (match.Success)
            {
                DateTime input;
                bool isCorrectDate = DateTime.TryParse(match.Value, culture.DateTimeFormat,DateTimeStyles.None, out input);
                if (!isCorrectDate) return "You enter an incorrect date";
                else date.date = input;
            } 
            
            return await date.BuildResult();
        }
    }
}