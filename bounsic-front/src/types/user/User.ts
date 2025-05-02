interface User {
  id_user: number;
  username: string;
  name: string;
  email: string;
  role: string;
  country: string;
  phone: number;
  member_since: Date;
  profile_img: string;
  preferences: {
    background: string;
    typography: string;
    language: string;
    theme: 'dark' | 'light'
  };
}
export default User;