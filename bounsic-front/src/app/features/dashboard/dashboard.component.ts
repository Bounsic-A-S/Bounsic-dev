import {
  ChangeDetectionStrategy,
  Component,
  inject,
  OnInit,
} from '@angular/core';
import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { SearchBarComponent } from './searchBar/search-bar.component';
import { SongsCarouselComponent } from './songsCarousel/songs-carousel.component';
import { RouterModule } from '@angular/router';
import { SafeChoiceListComponent } from './safeChoicesList/safe-choices-list.component';
import { TrendingSongsComponent } from './trendingSongs/trending-songs.component';
import { ArtistListComponent } from './artistList/artist_list.component';
import { LastMonthSongsComponent } from './lastMonthSongs/last-month-songs.component';
import { TranslateModule } from '@ngx-translate/core';
import { ArtistService } from '@app/services/artist.service';
import { Observable } from 'rxjs';
import { CommonModule } from '@angular/common';
import { SongService } from '@app/services/song.service';
import DashboardSong from 'src/types/dashboard/DashboardSong';
import DashboardArtist from 'src/types/dashboard/DashboardArtist';
import { AuthService } from '@app/services/auth/auth.service';
import { BackgroundService } from '@app/services/background.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    NavbarAppComponent,
    SearchBarComponent,
    SongsCarouselComponent,
    RouterModule,
    SafeChoiceListComponent,
    TrendingSongsComponent,
    ArtistListComponent,
    LastMonthSongsComponent,
    TranslateModule,
    CommonModule
],
  templateUrl: './dashboard.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DashboardComponent implements OnInit {
  private authService = inject(AuthService);
  private artistService = inject(ArtistService);
  private songService = inject(SongService);
  private backgroundService = inject(BackgroundService);
  artists$!: Observable<DashboardArtist[]>;
  songSafeChoices$!: Observable<DashboardSong[]>;
  songRelated$!: Observable<DashboardSong[]>;
  bg$ : Observable<string> = this.backgroundService.background$;
  
  ngOnInit(): void {
    this.authService.userProfile$.subscribe((user) => {
      if (user?.email) this.getData(user.email);
      if (user && user.preferences) {
        this.backgroundService.setBackground(user.preferences.background);
        this.getLanguage(user.preferences.language);
        this.getCurrentTheme(user.preferences.theme);
      }
    });
  }
  private getData(email: string): void {
    this.artists$ = this.artistService.getArtistsByUser(email);
    this.songSafeChoices$ = this.songService.getSafeChoices(email);
    this.songRelated$ = this.songService.getRelatedSongs(email);
  }
  
  private getLanguage(language: string): void {
    const savedLanguage = localStorage.getItem('language');
    if (!savedLanguage && language) {
      localStorage.setItem('language', language);
    }
  }
  private getCurrentTheme(theme: string): void {
    if(!theme) return
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme !== theme || !document.documentElement.classList.contains(theme)) {
      document.documentElement.className = '';
      document.documentElement.classList.add(theme);
      localStorage.setItem('theme', theme);
    }
  }
}
