import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

from app import app

layout = html.Div(
    [
        # Welcome message
        html.Div(
            [
                html.H1("Welcome to Dental Studio Database!", className="text-center", style={"margin-top": "20px"}),
                html.P(
                    "This platform serves as the primary database for Dental Studio, designed to organize and "
                    "manage patient records, appointments, financial transactions, and other essential information "
                    "for providing excellent dental care.",
                    className="text-center",
                    style={"font-size": "1.2rem", "margin": "20px 0"}),

                html.P(
                    "If you have any questions or concerns, please feel free to contact the administrators.",
                    className="text-center",
                    style={"font-size": "1.2rem", "margin": "18px 0"}
                ),
            ],
            className="text-center"
        ),
        
        # Image gallery section
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="https://scontent.fmnl17-5.fna.fbcdn.net/v/t39.30808-6/292309926_428188879321915_3042902948479000520_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=cc71e4&_nc_eui2=AeF_eD1xB1CvGZbSkhL5bhJNTvyecU1zMtNO_J5xTXMy0zyjyviJ_sfSvXNkedz61FXtC1sgsuOqB5-inwE_4x7Q&_nc_ohc=SDnqFDlJDksQ7kNvgEb-jnq&_nc_zt=23&_nc_ht=scontent.fmnl17-5.fna&_nc_gid=AayvMiQkxQ4_LAo4wyIYv3_&oh=00_AYCkdTrRJNSN7HSCeb6f0OtnZgc_tR0kKaYJRnKsH0mDIw&oe=67254A35", className="img-fluid rounded", style={"margin-bottom": "15px"}), width=4),
                        dbc.Col(html.Img(src="https://penndentalmedicine.org/wp-content/uploads/2016/02/shutterstock_2195411221-scaled-1024x683.jpg", className="img-fluid rounded", style={"margin-bottom": "15px"}), width=4),
                        dbc.Col(html.Img(src="https://scontent.fmnl17-6.fna.fbcdn.net/v/t1.6435-9/100481505_10213310576278214_9046095530840555520_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=7b2446&_nc_eui2=AeH_nfoRuArozBKaJa9nyOnIF7ypY-quLP8XvKlj6q4s_1MJX-rrauIgFrhD_Lb1hrslZrYEZNUsVyG3lf5z1yQq&_nc_ohc=x_saMDBqcboQ7kNvgFJI3yZ&_nc_zt=23&_nc_ht=scontent.fmnl17-6.fna&_nc_gid=AGnmzoGm-WAC3GgAJOdhuHM&oh=00_AYAzkfTKRAAK0AzuiV5W-AkThK-7BlEQJLDe9OK3aDwDeA&oe=6746CA21", className="img-fluid rounded", style={"margin-bottom": "15px"}), width=4),
                    ],
                    className="justify-content-center"
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="https://fermeliadental.com/wp-content/uploads/2019/05/benefits-of-regular-dental-visits-1080x675.jpeg", className="img-fluid rounded", style={"margin-bottom": "15px"}), width=4),
                        dbc.Col(html.Img(src="https://gallodental.com/wp-content/uploads/cosmetic-dentist-2112.jpg", className="img-fluid rounded", style={"margin-bottom": "15px"}), width=4),
                        dbc.Col(html.Img(src="https://scontent.fmnl17-5.fna.fbcdn.net/v/t1.6435-9/79015074_10213347036349693_1712055723183046656_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=7b2446&_nc_eui2=AeG40kDQKf6er8euDmF5Tv7a7CopOeQlZTDsKik55CVlMGc-stMc2RNP0-a1OPvqlyxgWS6GBPSu9I22YbVZeRAd&_nc_ohc=jtH-jhw7YIUQ7kNvgGZq7ms&_nc_zt=23&_nc_ht=scontent.fmnl17-5.fna&_nc_gid=AjOMcycTT2ypUZLSAkiIos8&oh=00_AYBP2q1-axV3XZeskR3EpYmdSxET4NFePzsPadSj_E1cPg&oe=6746D290", className="img-fluid rounded", style={"margin-bottom": "15px"}), width=4),
                    ],
                    className="justify-content-center"
                ),
            ]
        )
    ],
    style={"padding": "40px"}
)