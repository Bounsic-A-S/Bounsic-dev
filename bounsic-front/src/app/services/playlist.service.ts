import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { environment } from '../../environments/environment.dev';
import LibraryPlaylist from 'src/types/playlist/LIbraryPlaylist';
import Playlist from 'src/types/playlist/Playlist';

@Injectable({
  providedIn: 'root'
})
export class PlaylistService {
  private apiUrl = environment.apiUrl;
  private playlistsSubject = new BehaviorSubject<LibraryPlaylist[]>([]);
  private playlists$ = this.playlistsSubject.asObservable();

  constructor(private http: HttpClient) { }

  getAllPlaylist(): Observable<LibraryPlaylist[]> {
    if (this.playlistsSubject.value.length > 0) {
      return this.playlists$;
    }

    return this.http.get<any[]>(`${this.apiUrl}/user/playlists/user/1`).pipe(
      tap((playlists) => {
        this.playlistsSubject.next(playlists);
      }),
      catchError((err) => {
        console.error('Error al obtener playlists:', err);
        return of([]);
      })
    );
  }

  getPlaylistById(playlistId: string): Observable<Playlist> {
    return this.http.get<any>(`${this.apiUrl}/playlist/${playlistId}`).pipe(
      catchError((err) => {
        console.error('Error al obtener playlist:', err);
        return of({
          id: "0",
          title: "",
          img_url: "",
          updated_at: new Date(),
          songs: [],
          isPublic:false
        });
      })
    );
  }

  refreshPlaylists(): void {
    this.getAllPlaylist().subscribe();
  }
}
