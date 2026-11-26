using System;
using System.Diagnostics;
using System.Text.Json;
using System.Threading;
using System.Windows.Automation;

if (args.Length != 1 || !int.TryParse(args[0], out var targetId) || targetId <= 0)
{
    throw new ArgumentException("Expected one application process ID.");
}
using var target = Process.GetProcessById(targetId);
var condition = new PropertyCondition(AutomationElement.AutomationIdProperty, "ReadRaster");
var deadline = Stopwatch.StartNew();
while (deadline.Elapsed < TimeSpan.FromSeconds(12))
{
    target.Refresh();
    if (target.HasExited)
    {
        break;
    }
    if (target.MainWindowHandle != IntPtr.Zero)
    {
        var window = AutomationElement.FromHandle(target.MainWindowHandle);
        if (window.Current.ProcessId == targetId && window.Current.AutomationId == "RasterReadbackWindow")
        {
            var button = window.FindFirst(TreeScope.Descendants, condition);
            if (button is not null && button.Current.IsEnabled)
            {
                var buttonId = button.Current.AutomationId;
                ((InvokePattern)button.GetCurrentPattern(InvokePattern.Pattern)).Invoke();
                Console.WriteLine(JsonSerializer.Serialize(new
                {
                    WindowAutomationId = "RasterReadbackWindow",
                    ButtonAutomationId = buttonId,
                    Pattern = "Invoke",
                    SeparateProcess = targetId != Environment.ProcessId
                }));
                return;
            }
        }
    }
    Thread.Sleep(120);
}
throw new InvalidOperationException("Windows UI Automation did not find the enabled ReadRaster button.");
