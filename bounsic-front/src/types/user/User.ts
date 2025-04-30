interface User {
  id_user: number;
  username: string;
  name: string;
  last_name: string;
  email: string;
  role: string;
  profile_img: string;
  preferences: {
    background: string;
    typography: string;
    language: string;
  };
}
export default User;