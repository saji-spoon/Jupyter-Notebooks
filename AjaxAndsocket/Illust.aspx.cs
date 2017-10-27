using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using SocketToPythonCS;


namespace TrainingManagementWeb.Omake
{
    public partial class Illust : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (IsPostBack) return;

            

            if(Request.Form.Count != 0)
            {
                Response.ClearContent();
                try
                {
                    var res = MLCommunication.TestCommunication(13000, Request.Form["trainData"]);
                    Response.Write("recieved\n");
                    Response.Write(res);
                }
                catch (Exception ex)
                {
                    Response.Write("failed\n");
                }
 
                /*
                foreach (string key in Request.Form.Keys) 
                {
                    Response.Write(Request.Form[key].ToString());
                    Response.Write("\n");
                }*/

                Response.End();
                return;
            }
            else if(Request.HttpMethod == "POST")
            {
                Response.ClearContent();
                Response.Write("post no param received\n");
                Response.End();
                return;
            }
        }
    }
}