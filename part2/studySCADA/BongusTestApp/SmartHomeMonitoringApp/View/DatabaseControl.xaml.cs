using MahApps.Metro.Controls;
using MySqlConnector;
using Newtonsoft.Json;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SmartHomeMonitoringApp.View
{
    /// <summary>
    /// DatabaseControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class DatabaseControl : UserControl
    {

        public bool IsConnected { get; set; }
        public DatabaseControl()
        {
            InitializeComponent();
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            TxbBrokerUrl.Text = Commons.BROKERHOST;
            TxbMqttTopic.Text = Commons.MQTTTOPIC;
            TxtConnString.Text = Commons.MYSQL_CONNSTRING;

            IsConnected = false; // 아직 접속이 되어 있지 않음
            BtnConnDb.IsChecked = false;
        }

        private void BtnConnDb_Click(object sender, RoutedEventArgs e)
        {
            // 토글버튼 체크(1:접속 2:접속 끊기) 이벤트 핸들러
            if (IsConnected == false)
            {


                Commons.MQTT_CLIENT = new uPLibrary.Networking.M2Mqtt.MqttClient(Commons.BROKERHOST);

                try
                {
                    // MQTT subscribe (구독할) 로직
                    if (Commons.MQTT_CLIENT.IsConnected == false)
                    {
                        // MQTT 접속
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Connect("MONITOR");
                        Commons.MQTT_CLIENT.Subscribe(new string[] { Commons.MQTTTOPIC }, new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE });
                    }
                    UpdateLog(">>> MQTT Broker Connected");

                    BtnConnDb.IsChecked = true;
                    IsConnected = true; // 예외 발생하면 바뀔 필요 없음
                }
                catch
                {
                    // pass/
                }
            }
            else
            {
                BtnConnDb.IsChecked = false;
                IsConnected = false;
            }

        }
        private void UpdateLog(string msg)
        {
            this.Invoke(() =>
            {
                TxtLogs.Text += msg;
            });
        }


        // Substribe가 발생할 때 이벤트 핸들러
        private void MQTT_CLIENT_MqttMsgPublishReceived(object sender, uPLibrary.Networking.M2Mqtt.Messages.MqttMsgPublishEventArgs e)
        {
            var msg = Encoding.UTF8.GetString(e.Message);
            UpdateLog(msg);
            SetToDataBase(msg, e.Topic); // 실제 DB에 저장 처리
        }

        // DB 저장 처리 메서드
        private void SetToDataBase(string msg, string topic)
        {
           var currValue = JsonConvert.DeserializeObject<Dictionary<string, string>>(msg);
           if (currValue != null)
            {
                //Debug.WriteLine(currValue["Home_Id"]);
                //Debug.WriteLine(currValue["Room_Name"]);
                //Debug.WriteLine(currValue["Sensing_DateTime"]);
                //Debug.WriteLine(currValue["Temp"]);
                //Debug.WriteLine(currValue["Humid"]);

                try
                {
                    using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
                    {
                        if(conn.State == System.Data.ConnectionState.Closed) conn.Open();
                        string inQuery = "INSERT INTO smarthomesensor ...";

                        MySqlCommand cmd = new MySqlCommand(inQuery, conn);
                        cmd.Parameters.AddWithValue("@Home_Id", currValue["Home_Id"]);
                        cmd.Parameters.AddWithValue("@Room_Name", currValue["Room_Name"]);
                        cmd.Parameters.AddWithValue("@Sensing_DateTime", currValue["Sensing_DateTime"]);
                        cmd.Parameters.AddWithValue("@Temp", currValue["Temp"]);
                        cmd.Parameters.AddWithValue("@Humid", currValue["Humid"]);

                        if (cmd.ExecuteNonQuery()==1)
                        {
                            UpdateLog("DB 저장 완료");
                        }
                        else
                        {
                            UpdateLog("DB 저장 실패");
                        }
                    }
                }
                catch(Exception ex) 
                {
                    UpdateLog(ex.Message);
                }
            }
        }
    }
}
