import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment.dev';

@Injectable({
  providedIn: 'root'
})
export class PlaylistService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}
  getAllPlaylist(): Observable<any> {
    return this.http.get(`${this.apiUrl}/playlist/all`);
  }
  getPlaylistById(id:string): Observable<any> {
    return this.http.get(`${this.apiUrl}/playlist/${id}`);
  }
}
