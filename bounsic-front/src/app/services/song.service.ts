import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, catchError, Observable, of, tap } from 'rxjs';
import { environment } from '../../environments/environment.dev';
import DashboardSong from 'src/types/dashboard/DashboardSong';
import Song from 'src/types/Song';

@Injectable({
  providedIn: 'root'
})
export class SongService {
  private apiUrl = environment.apiUrl;
  private songSafeChoicesSubject = new BehaviorSubject<DashboardSong[]>([]);
  private songSafeChoices$ = this.songSafeChoicesSubject.asObservable();
  private songRelatedSubject = new BehaviorSubject<DashboardSong[]>([]);
  private songRelated$ = this.songSafeChoicesSubject.asObservable();


  constructor(private http: HttpClient) {}
  getData(title:string): Observable<any> {
    return this.http.get(`${this.apiUrl}/song/title/${title}`);
  }
  getById(id: string): Observable<Song> {
    return this.http.get<Song>(`${this.apiUrl}/song/id/${id}`).pipe(
      tap((song) => {
        return song;
      }),
      catchError((err) => {
        console.error('Error al obtener la canción:', err);
        return of({} as Song);
      })
    );
  }
  getSafeChoices (email: string): Observable<DashboardSong[]> {
    if(this.songSafeChoicesSubject.value.length > 0) {
      return this.songSafeChoices$;
    }
    return this.http.post<any>(`${this.apiUrl}/song/safeChoice`, { email: email }).pipe(
      tap((songSafeChoices) => {
        this.songSafeChoicesSubject.next(songSafeChoices);
      }),
      catchError((err) => {
        console.error('Error al obtener artistas:', err);
        return of([]);
      })  
    );
  }
  getRelatedSongs (email: string): Observable<DashboardSong[]> {
    if(this.songRelatedSubject.value.length > 0) {
      return this.songRelated$;
    }
    return this.http.post<any>(`${this.apiUrl}/song/getRelated`, { email: email }).pipe(
      tap((songsRelated) => {
        this.songRelatedSubject.next(songsRelated);
      }),
      catchError((err) => {
        console.error('Error al obtener artistas:', err);
        return of([]);
      })  
    );
  }
}
