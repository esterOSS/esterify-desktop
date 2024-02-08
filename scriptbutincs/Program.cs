/*
 * EsterifyScript.cs
 * rewritten from python to c# by: @jaydnreal
 * please note: this needs to be run in the directory of the esterify script after compilation.
 * i guess i could have made it more portable, but i didn't.
 */

using System;
using System.IO;
using System.Diagnostics;
using System.Threading;

namespace Esterify
{
    class EsterifyScript
    {
        // entry point of the script; checks for superuser rights before proceeding
        static void Main()
        {
            if (!IsUserSuperuser())
            {
                Console.WriteLine("This script must be run with superuser rights.");
                Environment.Exit(1);
            }

            ConfirmAndExecuteInstallation();
        }

        // confirms with the user before proceeding with the installation
        static void ConfirmAndExecuteInstallation()
        {
            Console.WriteLine("This operation will install the icons, font, and edit the application shortcuts (potentially dangerous).\n");
            Console.WriteLine("Are you absolutely sure you would like this script to make changes to your system? (Y/N)");

            string userChoice = Console.ReadLine();
            if (userChoice.Equals("Y", StringComparison.OrdinalIgnoreCase))
            {
                StartCountdown(5);
                PerformInstallationTasks();
                Console.WriteLine("The settings are set! Now reboot your system.");
            }
            else if (userChoice.Equals("N", StringComparison.OrdinalIgnoreCase))
            {
                Console.WriteLine("Operation cancelled by the user.");
            }
            else
            {
                Console.WriteLine("Invalid choice. Operation aborted.");
            }

            Console.WriteLine("Press Enter to exit!");
            Console.ReadLine();
        }

        // starts a countdown before beginning the installation, providing a buffer for the user to cancel if needed
        static void StartCountdown(int seconds)
        {
            for (int i = seconds; i > 0; i--)
            {
                Console.WriteLine(i.ToString());
                Thread.Sleep(1000); // sleep for 1 second
            }
            ExecuteShellCommand("clear", "");
        }

        // coordinates the installation tasks
        static void PerformInstallationTasks()
        {
            CopyEstericons();
            SetGnomeSettings();
        }

        // copies the estericons folder to the appropriate directory
        static void CopyEstericons()
        {
            string sourceDir = Path.Combine(Directory.GetCurrentDirectory(), "estericons");
            string destinationDir = "/usr/share/icons/estericons/";
            CopyDirectory(sourceDir, destinationDir);
            Console.WriteLine("The icons have been copied to `/usr/share/icons/`.");
        }

        // sets gnome settings using gsettings commands
        static void SetGnomeSettings()
        {
            ExecuteShellCommand("gsettings", "set org.gnome.desktop.interface icon-theme 'estericons'");
        }

        // checks if the current user is the superuser
        static bool IsUserSuperuser()
        {
            using (var process = new Process())
            {
                process.StartInfo.FileName = "id";
                process.StartInfo.Arguments = "-u";
                process.StartInfo.UseShellExecute = false;
                process.StartInfo.RedirectStandardOutput = true;
                process.Start();

                string output = process.StandardOutput.ReadToEnd();
                process.WaitForExit();

                return output.Trim() == "0";
            }
        }

        // executes a shell command
        static void ExecuteShellCommand(string command, string arguments)
        {
            using (var process = new Process())
            {
                process.StartInfo.FileName = command;
                process.StartInfo.Arguments = arguments;
                process.StartInfo.UseShellExecute = false;
                process.StartInfo.RedirectStandardOutput = true;
                process.Start();

                process.WaitForExit();
            }
        }

        // copies a directory and its contents to a new location
        static void CopyDirectory(string sourceDir, string destinationDir)
        {
            DirectoryInfo dir = new DirectoryInfo(sourceDir);

            if (!dir.Exists)
            {
                throw new DirectoryNotFoundException($"Source directory does not exist or could not be found: {sourceDir}");
            }

            if (!Directory.Exists(destinationDir))
            {
                Directory.CreateDirectory(destinationDir);
            }

            FileInfo[] files = dir.GetFiles();
            foreach (FileInfo file in files)
            {
                string tempPath = Path.Combine(destinationDir, file.Name);
                file.CopyTo(tempPath, false);
            }

            DirectoryInfo[] dirs = dir.GetDirectories();
            foreach (DirectoryInfo subdir in dirs)
            {
                string tempPath = Path.Combine(destinationDir, subdir.Name);
                CopyDirectory(subdir.FullName, tempPath);
            }
        }
    }
}
