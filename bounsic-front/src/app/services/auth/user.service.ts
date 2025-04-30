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

  constructor(private http: HttpClient) {}
  getUserByEmail(email: string): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/user/${email}`);
  }
  setLanguage(language: string,id:number): Observable<boolean> {
    return this.http.put<boolean>(`${this.apiUrl}/user/language/${id}`,{"language": language});
  }
  setBackground(background: string,id:number): Observable<boolean> {
    return this.http.put<boolean>(`${this.apiUrl}/user/background/${id}`,{"background": background});
  }}