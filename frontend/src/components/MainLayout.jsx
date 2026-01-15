import Navbar from "./Navbar";
import "../styles/common.css";

export default function MainLayout({ children }) {
  return (
    <div className="app-layout">
      <Navbar />
      <main className="dashboard">{children}</main>
    </div>
  );
}
