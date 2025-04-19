import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment.dev';

@Injectable({
  providedIn: 'root',
})
export class ArtistService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}
  getArtistsByUser(email: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/artist/by_user`, { email: email });
  }
}
