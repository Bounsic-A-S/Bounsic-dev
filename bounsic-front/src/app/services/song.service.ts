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
  //safe choices
  private songSafeChoicesSubject = new BehaviorSubject<DashboardSong[]>([]);
  private songSafeChoices$ = this.songSafeChoicesSubject.asObservable();
  //related songs
  private songRelatedSubject = new BehaviorSubject<DashboardSong[]>([]);
  private songRelated$ = this.songRelatedSubject.asObservable();
  //last month
  private songLastMonthSubject = new BehaviorSubject<DashboardSong[]>([]);
  private songLastMonth$ = this.songLastMonthSubject.asObservable();
  // trending
  private songTrendingSubject = new BehaviorSubject<DashboardSong[]>([]);
  private songTrending$ = this.songTrendingSubject.asObservable();

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
        console.error('Error al obtener safe choices:', err);
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
        console.error('Error al obtener related songs:', err);
        return of([]);
      })  
    );
  }
  getLastMonthSongs (email: string): Observable<DashboardSong[]> {
    if(this.songLastMonthSubject.value.length > 0) {
      return this.songLastMonth$;
    }
    return this.http.post<any>(`${this.apiUrl}/song/lastMonth`, { email: email }).pipe(
      tap((songsLastMonth) => {
        this.songLastMonthSubject.next(songsLastMonth);
      }),
      catchError((err) => {
        console.error('Error al obtener last month songs:', err);
        return of([]);
      })  
    );
  }
  getTrendingSongs (): Observable<DashboardSong[]> {
    if(this.songTrendingSubject.value.length > 0) {
      return this.songTrending$;
    }
    return this.http.get<any>(`${this.apiUrl}/song/top12`).pipe(
      tap((songTrending) => {
        this.songTrendingSubject.next(songTrending);
      }),
      catchError((err) => {
        console.error('Error al obtener last month songs:', err);
        return of([]);
      })  
    );
  }
  //search
  searchSongByTitle (title : string): Observable<DashboardSong[]> {
    return this.http.get<any>(`${this.apiUrl}/song/search/${title}`).pipe(
      catchError((err) => {
        console.error('Error en la busqeuda:', err);
        return of([]);
      })  
    );
  }
}
