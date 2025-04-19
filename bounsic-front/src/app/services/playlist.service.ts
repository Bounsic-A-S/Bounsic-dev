import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, switchMap, tap } from 'rxjs/operators';
import { environment } from '../../environments/environment.dev';

@Injectable({
  providedIn: 'root'
})
export class PlaylistService {
  private apiUrl = environment.apiUrl;
  private playlistsSubject = new BehaviorSubject<any[]>([]);
  private playlists$ = this.playlistsSubject.asObservable();

  constructor(private http: HttpClient) {}

  getAllPlaylist(): Observable<any[]> {
    if (this.playlistsSubject.value.length > 0) {
      return this.playlists$;
    }

    return this.http.get<any[]>(`${this.apiUrl}/playlist/all`).pipe(
      tap((playlists) => {
        this.playlistsSubject.next(playlists);
      }),
      catchError((err) => {
        console.error('Error al obtener playlists:', err);
        return of([]);
      })
    );
  }

  getPlaylistById(playlistId: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/playlist/${playlistId}`).pipe(
      catchError((err) => {
        console.error('Error al obtener playlist:', err);
        return of(null);
      })
    );
  }

  refreshPlaylists(): void {
    this.getAllPlaylist().subscribe();
  }
}
