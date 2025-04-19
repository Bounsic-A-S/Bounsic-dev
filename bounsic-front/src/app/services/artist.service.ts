import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, catchError, Observable, of, tap } from 'rxjs';
import { environment } from '../../environments/environment.dev';

@Injectable({
  providedIn: 'root',
})
export class ArtistService {
  private apiUrl = environment.apiUrl;
  private artistsSubject = new BehaviorSubject<any[]>([]);
  private artists$ = this.artistsSubject.asObservable();

  constructor(private http: HttpClient) {}
  getArtistsByUser(email: string): Observable<any> {
    if(this.artistsSubject.value.length > 0) {
      return this.artists$;
    }
    return this.http.post<any>(`${this.apiUrl}/artist/by_user`, { email: email }).pipe(
      tap((artists) => {
        this.artistsSubject.next(artists);
      }),
      catchError((err) => {
        console.error('Error al obtener artistas:', err);
        return of([]);
      })  
    );
  }
}