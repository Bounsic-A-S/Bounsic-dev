import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { SearchBarComponent } from './searchBar/search-bar.component';
import { SongsCarouselComponent } from './songsCarousel/songs-carousel.component';
import { RouterModule } from '@angular/router';
import { SafeChoiceListComponent } from './safeChoicesList/safe-choices-list.component';
import { TrendingSongsComponent } from "./trendingSongs/trending-songs.component";
import { ArtistListComponent } from "./artistList/artist_list.component";
import { LastMonthSongsComponent } from "./lastMonthSongs/last-month-songs.component";
import { TranslateModule } from '@ngx-translate/core';
import { ArtistService } from '@app/services/artist.service';
import { Observable } from 'rxjs';
import { CommonModule } from '@angular/common';
import { SongService } from '@app/services/song.service';
import DashboardSong from 'src/types/dashboard/DashboardSong';
import DashboardArtist from 'src/types/dashboard/DashboardArtist';
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
    TranslateModule,CommonModule
],
  templateUrl: './dashboard.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DashboardComponent {
  private artistService = inject(ArtistService);
  private songService = inject(SongService);
  artists$!: Observable<DashboardArtist[]>;
  songSafeChoices$!: Observable<DashboardSong[]>


  ngOnInit() : void {
    this.artists$ = this.artistService.getArtistsByUser("juan.patino.2022@upb.edu.co");
    this.songSafeChoices$ = this.songService.getSafeChoices("juan.patino.2022@upb.edu.co");
  }

}
