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
import { BehaviorSubject, Observable } from 'rxjs';
import { CommonModule } from '@angular/common';
import { SongService } from '@app/services/song.service';
import DashboardSong from 'src/types/dashboard/DashboardSong';
import DashboardArtist from 'src/types/dashboard/DashboardArtist';
import { AuthService } from '@app/services/auth/auth.service';

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
    CommonModule,
  ],
  templateUrl: './dashboard.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DashboardComponent implements OnInit {
  private authService = inject(AuthService);
  private artistService = inject(ArtistService);
  private songService = inject(SongService);

  artists$!: Observable<DashboardArtist[]>;
  songSafeChoices$!: Observable<DashboardSong[]>;
  bg$ = new BehaviorSubject<string>('bg-bounsic-gradient');

  ngOnInit(): void {
    this.authService.userProfile$.subscribe((user) => {
      if (user) this.getData(user.email);
      if (user && user.preferences) {
        this.getBackground(user.preferences.background);
        this.getLanguage(user.preferences.language);
        this.getCurrentTheme(user.preferences.theme);
      }
    });
  }
  private getData(email: string): void {
    this.artists$ = this.artistService.getArtistsByUser(email);
    this.songSafeChoices$ = this.songService.getSafeChoices(email);
  }

  private getBackground(background: string): void {
    const savedBackground = localStorage.getItem('background');
    if (savedBackground) {
      this.bg$.next(savedBackground);
    } else {
      this.bg$.next(background);
      localStorage.setItem('background', background);
    }
  }
  private getLanguage(language: string): void {
    const savedLanguage = localStorage.getItem('language');
    if (!savedLanguage && language !== null) {
      localStorage.setItem('language', language);
    }
  }
  getCurrentTheme(theme : string): void {
    if(theme) {
      document.documentElement.classList.add(theme)
      localStorage.setItem('theme', theme);
      console.log(theme)
    }
  }
}
