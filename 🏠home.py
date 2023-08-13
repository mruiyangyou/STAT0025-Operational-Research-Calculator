import streamlit as st 
import streamlit.components.v1 as com

st.set_page_config(layout='wide',
                   page_title='Home',
                   page_icon = '🏠')
html = """
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.5/dist/umd/popper.min.js" integrity="sha384-Xe+8cL9oJa6tN/veChSP7q+mnSPaj5Bcu9mPX5F5xIGE0DVittaqT5lorf0EI7Vk" crossorigin="anonymous"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
    <link rel="canonical" href="https://getbootstrap.com/docs/5.2/examples/headers/">
    <script src="https://kit.fontawesome.com/eb511fb6e6.js" crossorigin="anonymous"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather&family=Montserrat:wght@100;400;900&family=Nanum+Gothic&family=Oswald&family=Sacramento&display=swap" rel="stylesheet">
    <style>
        h1, h2, h3, h4, h5, h6 {
            font-family: "Montserrat-Bold";
           
        }
        
        h3 {
            
            font-size: 1.5rem;
            
        }
        

        .title-heading {
            font-family: 'Oswald';
            font-size: 5rem;
            line-height: 1.5;
            font-weight: 900;
        
        }
        
        .titlecolor{
            background-color: #213FFF;
            color: white;
        }
        
        .container-fluid {
            padding: 3% 15% 7%;
            margin-left: 0;
            margin-right: 0;
        }
        
        
        .col-lg-6-img {
            display: flex;
            align-items: center; /* vertically center */
            justify-content: center; /* horizontally center */
        
        }
        
        .title-img {
            max-width: 100%;
            height: auto;
            padding: auto;
        }
        
         .title-text {
            padding-top: 1ch;
            font-size: 1.2rem;
            font-family: 'Nanum Gothic';
         }

         #features {
            padding: 7% 7%;
            background-color: white;
            position: relative;
            z-index: 1;
        }
        
        .feature-p {
            color: #8f8f8f;
            font-family: 'Nanum Gothic';
        }
        
        .feature-icon {
            color: #213FFF;
            margin-bottom: 1rem;
        }
        
        .feature-icon:hover {
            color: #21aaff;
        }
        
        .feature-box {
            text-align: center;
            padding: 5%;
        }
        

        #cta {
            background-color: #213FFF;
            text-align: center;
            padding: 5% 15%;
        }
        
        .cta-text {
            font-size: 3rem;
            color: white;
            font-family:'Oswald' ;
            padding-bottom: 1ch;
        }
        
        /* footer */
        
        #footer {
            background-color: #fff;
            text-align: center;
            padding: 5% 30% 2%;
        }
        
    
        @media (max-width:1028px) {
            .title-img {
               position: static;
               transform: rotate(0);
               width: 100%; /* adjust this as per your needs */
               margin: auto; /* to center the image on smaller screens */
            }
        
        #title {
                text-align: center;
            }
        }
        
    
    </style>



    <section id = 'title'> 

    <div class = 'row titlecolor container-fluid'>
        <div class="col-lg-6">
          <h1 class = 'title-heading'>STAT0025 Calculator Tool</h1>
          <div class = 'title-text'>
          <p>This tools can easily help understand the process of calculation, save your time when you are doing the iteration and provide 
              you with the accurate answers to check. It is comprised by three parts.
          </p>
          <ul>
              <li>
                  Graphic Solution: Solve optimization problems from two parties
              </li>
              <li>
                  Generalized Simplex Viusalization 1: Show each step of the caulcation process of big M Method
              </li>
              <li>
                Generalized Simplex Viusalization 2: Show each step of the caulcation process of Simplex Method
              </li>
              <li>
                  Markov dynamic programming: Quickly calculate the answers.
              </li>
          </ul>
          </div>
      </div> 
      
      <div class="col-lg-6 col-lg-6-img">
          <img src="https://i.ibb.co/Y7bmgvj/research.jpg" alt="research" class="title-img" border="0" />
      </div>
     </div>
    </section>


    <section id ="features">
        <div class = 'row'>
            <div class="col-lg-4 feature-box">
            <i class="fa-solid fa-circle-check feature-icon fa-4x"></i>
            <h3>Easy to use</h3>
            <p class = 'feature-p'>So easy to use, type input give answers</p>
            </div>
            <div class="col-lg-4 feature-box">
            <i class="fa-solid fa-bullseye feature-icon fa-4x"></i>
            <h3>Accurate</h3>
            <p class = 'feature-p'>It strictly follow the process on the note</p>
            </div>
            <div class="col-lg-4 feature-box">
            <i class="fa-solid fa-heart feature-icon fa-4x"></i>
            <h3>Quick to implement</h3>
            <p class = 'feature-p'>It takes seconds to give the answers</p>
            </div>
        </div>
    </section>
      

    <section id="cta">
      <h3 class="cta-text">Start your comfortable learning journey with this website</h3>
    </section>

    
  <footer id="footer">
      <i class="fa-brands fa-twitter ft-img"></i>
      <i class="fa-brands fa-facebook-f ft-img"></i>
      <i class="fa-brands fa-instagram ft-img"></i>
      <i class="fa-solid fa-envelope ft-img"></i>
      <p class = 'ft-text'>© Copyright RuiyangYou</p>
  
  </footer>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>  

"""

# set the home page

com.html(html, height = 1600, scrolling=True)


markdown = """
<style>
.icon {
    color: white;
}

.center-content {
    display: flex;
    justify-content: center;
    width: 100%;
}

.margin-right {
    margin-right: 10px;
}
</style>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
<link rel="canonical" href="https://getbootstrap.com/docs/5.2/examples/headers/">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css" integrity="sha512-z3gLpd7yknf1YoNbCzqRKc4qyor8gaKU1qmn+CShxbuBusANI9QpRohGBreCFkKxLhei6S9CQXFEbbKuqLg0DA==" crossorigin="anonymous" referrerpolicy="no-referrer" />

<div class="center-content">
    <a href='https://github.com/mruiyangyou/STAT0025-Operational-Research-Calculator.git' class='btn btn-dark btn-lg db icon margin-right'>
    <i class="fa-brands fa-github icon"></i><span style="color: white;"> Github</span>
    </a>
    <a href='https://github.com/mruiyangyou/STAT0025-Operational-Research-Calculator.git' class='btn btn-dark btn-lg db icon'>
    <i class="fa-solid fa-bookmark icon"></i><span style="color: white;"> Notes</span>
    </a>
</div>
"""

st.markdown(markdown, unsafe_allow_html=True)
