using Bogus;
using MahApps.Metro.Controls;
using MahApps.Metro.Controls.Dialogs;
using Newtonsoft.Json;
using System;
using System.Diagnostics;
using System.Text;
using System.Threading;
using System.Windows;
using System.Windows.Documents;
using uPLibrary.Networking.M2Mqtt;

namespace FakeLotDeviceApp
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        Faker<SensorInfo> FakeHomeSensor { get; set; } = null;
        MqttClient client;
        Thread MqttThread { get; set; }
        public MainWindow()
        {
            InitializeComponent();

            InitFakeData();
        }

        private void InitFakeData()
        {
            var Rooms = new[] { "Bed", "Beth", "Living", "Dining" };

            FakeHomeSensor = new Faker<SensorInfo>()
                .RuleFor(s => s.Home_Id, "D101H703")
                .RuleFor(s => s.Room_Name, f => f.PickRandom(Rooms))
                .RuleFor(s => s.Sensing_DateTime, f => f.Date.Past(0))
                .RuleFor(s => s.Temp, f => f.Random.Float(20.0f, 30.0f))
                .RuleFor(s => s.Humid, f => f.Random.Float(40.0f, 64.0f));
        }

        private async void BtnConnect_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(TxtMqttBrokerIp.Text))
            {
                await this.ShowMessageAsync("오류", "브로커 아이피를 입력하세요");
                return;
            }

            // 브로커 아이피로 접속
            ConnectMqttBroker();
            // 하위의 로직을 무한 반복
            StartPublsh();

            // 가짜 스마트 홈 센서값을 만들어서 전달
            var info = FakeHomeSensor.Generate();

            // 센서값 MQTT 브로커에 전송

            // RtbLog에 출력
        }
        private void StartPublsh()
        {
            MqttThread = new Thread(() =>
                {
                    while (true)
                    {
                        //가짜 스마트홈 센서값 생성
                        SensorInfo Info = FakeHomeSensor.Generate();
                        // 릴리즈 (배포)때는 주석처리/삭제
                        Debug.WriteLine($"{Info.Home_Id} / {Info.Room_Name} / {Info.Sensing_DateTime} / {Info.Temp}");  
                        //객체 직렬화
                        var jsonValue = JsonConvert.SerializeObject(Info, Formatting.Indented);
                        // 센서값 MQTT 브로커에 전송(Publish)
                        client.Publish("SmartHome/IotData/",Encoding.Default.GetBytes(jsonValue));
                        // 스레드와 ui스레드간 충돌이 안 나도록 변경
                        this.Invoke(new Action(() =>
                        {
                            //// RtbLog에 출력
                            //FlowDocument flowDoc = new FlowDocument();
                            //Paragraph paragraph = new Paragraph();
                            //flowDoc.Blocks.Add(new Paragraph(new Run(jsonValue)));
                            //flowDoc.Blocks.Add(paragraph);
                            //RtbLog.Document = flowDoc;
                            RtbLog.AppendText(jsonValue);
                            RtbLog.ScrollToEnd(); // 스크롤 맨 밑으로 내리기
                        }));
                        // 1초 동안 대기
                        Thread.Sleep(1000);

                    }
                    // 가짜 스마트홈 센서값 생성

                    //
                });
            MqttThread.Start();
        }

        private void ConnectMqttBroker()
        {
            client = new MqttClient(TxtMqttBrokerIp.Text);
            client.Connect("SmartHomeDev"); //publish client ID를 지정
        }

        private void MetroWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if(client != null && client.IsConnected == true)
            { 
            client.Disconnect(); // 접속을 안 끊으면 메모리상에 계속 남아있음
            }

            if (MqttThread != null)
            {
                MqttThread.Abort();
            }
        }
    }
}
