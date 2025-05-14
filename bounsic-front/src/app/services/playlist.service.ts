import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { environment } from '../../environments/environment.dev';
import LibraryPlaylist from 'src/types/playlist/LIbraryPlaylist';
import Playlist from 'src/types/playlist/Playlist';
import Song from 'src/types/Song';

@Injectable({
  providedIn: 'root',
})
export class PlaylistService {
  private apiUrl = environment.apiUrl;
  private playlistsSubject = new BehaviorSubject<LibraryPlaylist[]>([]);
  private playlists$ = this.playlistsSubject.asObservable();

  constructor(private http: HttpClient) { }

  getAllPlaylist(user_id: number): Observable<LibraryPlaylist[]> {
    if (this.playlistsSubject.value.length > 0) {
      return this.playlists$;
    }

    this.loadPlaylists(user_id);
    return this.playlists$;
  }

  refreshPlaylists(user_id: number): void {
    this.loadPlaylists(user_id);
  }

  private loadPlaylists(user_id: number): void {
    this.http.get<LibraryPlaylist[]>(`${this.apiUrl}/user/playlists/user/${user_id}`)
      .pipe(
        tap(playlists => this.playlistsSubject.next(playlists)),
        catchError(err => {
          console.error('Error al obtener playlists:', err);
          this.playlistsSubject.next([]);
          return of([]);
        })
      )
      .subscribe();
  }

  getPlaylistById(playlistId: string): Observable<Playlist> {
    return this.http.get<any>(`${this.apiUrl}/playlist/${playlistId}`).pipe(
      catchError((err) => {
        console.error('Error al obtener playlist:', err);
        return of({
          id: '0',
          title: '',
          img_url: '',
          updated_at: new Date(),
          songs: [],
          isPublic: false,
        });
      })
    );
  }
  getLikesCount(user_id: number): Observable<number> {
    return this.http
      .get<any>(`${this.apiUrl}/user/likes/count/${user_id}`)
      .pipe(
        catchError((err) => {
          console.error('Error al obtener likes:', err);
          return of(0);
        })
      );
  }
  getLikesPlaylist(user_id: number): Observable<Song[]> {
    return this.http.get<any>(`${this.apiUrl}/user/likes/${user_id}`).pipe(
      catchError((err) => {
        console.error('Error al obtener playlist:', err);
        return of([] as Song[]);
      })
    );
  }

  createPlaylist(data: FormData): Observable<boolean> {
    return this.http.post<any>(`${this.apiUrl}/playlist/create`, data).pipe(
      catchError((err) => {
        console.error('Error al crear playlist:', err);
        return of(false);
      })
    );
  }
}
