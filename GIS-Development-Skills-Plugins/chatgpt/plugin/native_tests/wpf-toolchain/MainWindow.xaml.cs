using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Text.Json;
using System.Windows;
using System.Windows.Automation.Peers;
using System.Windows.Automation.Provider;
using System.Windows.Interop;
using System.Windows.Threading;

namespace ToolchainSmoke;

public partial class MainWindow : Window
{
    private readonly string[] arguments = Environment.GetCommandLineArgs();
    private RasterResult? raster;
    private int clicks;
    private bool ImportMode => arguments.Length == 4 && arguments[1] is "--smoke" or "--external-uia";

    public MainWindow()
    {
        InitializeComponent();
        if (ImportMode)
        {
            ShowActivated = false;
            if (arguments[1] == "--smoke")
            {
                ShowInTaskbar = false;
                Opacity = 0;
            }
        }
    }

    private void ReadRaster(object sender, RoutedEventArgs eventArgs)
    {
        using var document = JsonDocument.Parse(File.ReadAllBytes(arguments[2]));
        var value = document.RootElement.GetProperty("raster");
        var shape = value.GetProperty("shape");
        var rows = shape[0].GetInt32();
        var columns = shape[1].GetInt32();
        var count = 0;
        var grid = value.GetProperty("values");
        if (grid.GetArrayLength() != rows)
        {
            throw new InvalidDataException("Raster row count differs from its declared shape.");
        }
        foreach (var row in grid.EnumerateArray())
        {
            if (row.GetArrayLength() != columns)
            {
                throw new InvalidDataException("Raster column count differs from its declared shape.");
            }
            foreach (var pixel in row.EnumerateArray())
            {
                if (pixel.ValueKind != JsonValueKind.Null)
                {
                    pixel.GetDouble();
                    count++;
                }
            }
        }
        raster = new RasterResult(value.GetProperty("crs").GetString()!, rows,
                                  columns, value.GetProperty("nodata").GetInt32(), count);
        ResultLabel.Text = $"{raster.Crs} | {raster.Rows} x {raster.Columns} | {raster.ValidCells} valid cells";
        clicks++;
        Dispatcher.BeginInvoke(DispatcherPriority.ApplicationIdle, new Action(WriteReceipt));
    }

    private void WindowLoaded(object sender, RoutedEventArgs eventArgs)
    {
        if (!ImportMode)
        {
            ReadRasterButton.IsEnabled = false;
            ResultLabel.Text = "Use the test harness to supply a raster readback file.";
            return;
        }
        if (arguments[1] == "--smoke")
        {
            var peer = new ButtonAutomationPeer(ReadRasterButton);
            var invoke = (IInvokeProvider)peer.GetPattern(PatternInterface.Invoke)!;
            invoke.Invoke();
        }
    }

    private void WriteReceipt()
    {
        var loaded = IsLoaded && new WindowInteropHelper(this).Handle != IntPtr.Zero;
        using var receipt = new FileStream(arguments[3], FileMode.CreateNew);
        JsonSerializer.Serialize(receipt, new
        {
            NativeWindowLoaded = loaded,
            AutomationPattern = "Invoke",
            Clicks = clicks,
            Raster = raster,
            Label = ResultLabel.Text,
            Runtime = RuntimeInformation.FrameworkDescription,
            Architecture = RuntimeInformation.ProcessArchitecture.ToString()
        });
        Application.Current.Shutdown(loaded && clicks == 1 && raster is not null ? 0 : 1);
    }

    private sealed record RasterResult(string Crs, int Rows, int Columns, int NoData, int ValidCells);
}
