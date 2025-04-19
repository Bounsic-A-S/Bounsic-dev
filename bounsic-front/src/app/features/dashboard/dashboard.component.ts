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
import { catchError, firstValueFrom, of } from 'rxjs';
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
    TranslateModule
],
  templateUrl: './dashboard.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DashboardComponent {
  private artistService = inject(ArtistService);
  artists: [] = [];

  async ngOnInit() {
    try {
      const response = await firstValueFrom(
        this.artistService.getArtistsByUser("induismo97@hotmail.com").pipe(
          catchError(error => {
            console.error('Error obteniendo datos:', error);
            return of([]);
          })
        )
      );

      if (response) {
        this.artists = response;
      }
    } catch (error) {
      console.error("Error en ngOnInit:", error);
    }
  }

}
