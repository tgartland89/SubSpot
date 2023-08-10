import React, { useState, useEffect } from "react";
import { Switch, Route } from "react-router-dom";
import Home from "./Home";
import LoginComponent from "./Login";
import SignUp from "./SignUp";
import DashboardPage from "./DashboardPage";
import NavBar from "./NavBar";
import NotFound from "./NotFound";
import SubsDetails from "./SubDetails";
import { loginUser } from "./api";
import { useAuth } from "../AuthContext";
import TeacherDashboard from "./TeacherDashboard";
import SubstituteDashboard from "./SubstituteDashboard";
import AdminDashboard from "./AdminDashboard";

function About() {
  return (
    <div>
    <h2 className="underlined-heading">About SubSpot</h2>
  <p>
    SubSpot is the visionary brainchild of Thomas Gartland, a distinguished alumnus of Flatiron's intensive 15-week Full Stack Software Boot Camp. Born into a lineage of educators, with a fourth-grade teacher as his own mother, Thomas's journey in creating SubSpot was deeply influenced by the need for efficient solutions in the education sector.
  </p>
  <p>
    Armed with insights from his mother's experiences and his extensive software development training, Thomas set out to revolutionize the way substitute teachers are discovered and engaged. His mission was to craft a platform that would not only streamline the process for educators but also pave the way for a more collaborative and empowered teaching community.
  </p>
  <p>
    Drawing inspiration from the likes of "Lyft" and "Uber," Thomas envisioned SubSpot as more than just a tool; it's a catalyst for transformative change in education. Beyond the convenience it offers, SubSpot is a testament to the fusion of technology and empathy, addressing a critical need while fostering a sense of support and unity among educators.
  </p>
  <p>
    Thomas Gartland's aspiration isn't limited to financial success; it's rooted in a commitment to enhancing the educational experience. By bridging the gap between educators and substitute teachers, SubSpot creates an ecosystem where seamless transitions are the norm, contributing to a cohesive and efficient learning environment.
  </p>
  <p>
    As SubSpot continues to unfold, it stands as a beacon of innovation, testament to the potential of a single individual's vision to drive transformative impact. Thomas's journey, from boot camp graduate to education tech visionary, embodies the power of determination and passion in shaping the future of education. With SubSpot, educators can look forward to a brighter future, where finding substitutes is as simple as a few clicks.
  </p>
  <p>
    SubSpot isn't just a platform; it's a testament to the potential of human ingenuity, the marriage of technology and education, and the ripple effect of positive change that emerges when a community of educators come together with a shared goal.
  </p>
</div>
  );
}
function App() {
   // eslint-disable-next-line
  const [userData, setUserData] = useState({ role: '', teacher_user_id: null });
  const { user, login } = useAuth();
  // eslint-disable-next-line
  const [isLoading, setIsLoading] = useState(true);
  const [teacherId, setTeacherId] = useState(null); 
  useEffect(() => {
    const urlSearchParams = new URLSearchParams(window.location.search);
    const email = urlSearchParams.get("email");
    const password = urlSearchParams.get("password");
  
    if (email && password) {
      loginUser(email, password)
        .then((data) => {
          console.log("API Response Data:", data); 
          login(data);
          console.log("User role after login:", data.role);
          setTeacherId(data.teacherId);
          window.history.replaceState({}, document.title, window.location.pathname);
        })
        .catch((error) => {
          console.error("Error occurred during login:", error);
        });
    } else {
      setIsLoading(false);
    }
  }, [login]);
  

  console.log("User Role:", user?.role);

  return (
    <div className="container warm-blue-bg"> 
      <NavBar />
      <div className="content">
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/login" component={LoginComponent} />
          <Route path="/signup" component={SignUp} />
          <Route path="/about" component={About} />
          <Route path="/dashboard" render={() => <DashboardPage userRole={user?.role} />} />
          <Route path="/teacher-dashboard" render={() => {
          console.log("Passed teacherId to TeacherDashboard:", teacherId); // Add this line
         return <TeacherDashboard userRole={user?.role} userName={user?.name} userEmail={user?.email} teacherId={teacherId} />;}}/>
          <Route path="/substitute-dashboard" component={SubstituteDashboard} />
          <Route path="/admin-dashboard" component={AdminDashboard} />
          <Route path="/sub-details/:substituteId" component={SubsDetails} />
          <Route component={NotFound} />
        </Switch>
      </div>
    </div>
  );
}

export default App;