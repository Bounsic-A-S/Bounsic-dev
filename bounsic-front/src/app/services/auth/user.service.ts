import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment.dev';
import User from 'src/types/user/User';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }
  getUserByEmail(email: string): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/user/${email}`);
  }
  isSongLikedByUser(user_id:number,song_id:String): Observable<boolean> {
    return this.http.get<boolean>(`${this.apiUrl}/user/hasLike/${user_id}/${song_id}`);
  }
  registerUser(user: any): Observable<boolean> {
    return this.http.post<boolean>(`${this.apiUrl}/user/register`, user);
  }
  updateUser(user: any, id: number): Observable<boolean> {
    return this.http.put<boolean>(`${this.apiUrl}/user/update/${id}`, user);
  }
  setLanguage(language: string, id: number): Observable<boolean> {
    return this.http.put<boolean>(`${this.apiUrl}/user/language/${id}`, { "language": language });
  }
  setBackground(data: any, id: number): Observable<boolean> {
    return this.http.put<boolean>(`${this.apiUrl}/user/background/${id}`, data);
  }
}