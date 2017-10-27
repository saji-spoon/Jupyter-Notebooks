using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;

namespace SocketToPythonCS
{
    public class MLCommunication 
    {
        static string TestCommunication(int port, string data)
        {
            TcpClient client = new TcpClient("localhost", port);

            byte[] byteData = System.Text.Encoding.ASCII.GetBytes(data);

            NetworkStream stream = client.GetStream();

            stream.Write(byteData, 0, byteData.Length);

            //送り終わったらハーフクローズ
            client.Client.Shutdown(SocketShutdown.Send);

            int len = 0;
            byte[] buffer = new byte[3];
            var recieved = new List<byte>();
            while ((len = stream.Read(buffer, 0, buffer.Length)) != 0)
            {
                recieved.AddRange(buffer.Take(len));
            }

            stream.Close();
            client.Close();

            var resultStr = Encoding.UTF8.GetString(recieved.ToArray());

            return resultStr;
        }
    }

    class Program
    {


        static void Main(string[] args)
        {
            int port = 13000;

            var rand = new Random(2000);

            var trainData = new List<string>();
            for (int i=0; i<200; ++i)
            {
                var dt = new List<int> { rand.Next(0, 300), rand.Next(0, 300), rand.Next(0, 1+1) };

                trainData.Add(string.Join(",", dt));

                Console.WriteLine(string.Join(",", dt));
            }

            Console.WriteLine("trainData=====");

            Console.WriteLine(string.Join("\n", trainData));

            var dataStr = string.Join("\n", trainData);

            for (int i = 0; i < 10; ++i)
            {
                var resultStr = TestCommunication(port, dataStr);

                Console.Write(resultStr);
                Console.Write("\n");

                Console.Write("キーでもう一回送る");
                Console.ReadKey();
            }
            Console.Write("終了");
            Console.ReadKey();
        }
    }
}
