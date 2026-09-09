import { useAuth } from "./state/AuthContext.jsx";
import Chat from "./pages/Chat.jsx";
import Auth from "./pages/Auth.jsx";
import Toaster from "./components/Toaster.jsx";

export default function App() {
  const { user } = useAuth();
  return (
    <>
      {user ? <Chat /> : <Auth />}
      <Toaster />
    </>
  );
}
