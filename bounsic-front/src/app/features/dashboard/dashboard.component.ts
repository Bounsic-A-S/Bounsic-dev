import { ChangeDetectionStrategy, Component } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { SearchBarComponent } from './searchBar/search-bar.component';
import { SongsCarouselComponent } from './songsCarousel/songs-carousel.component';
import { RouterModule } from '@angular/router';
import { SafeChoiceListComponent } from './safeChoicesList/safe-choices-list.component';
import { TrendingSongsComponent } from "./trendingSongs/trending-songs.component";
import { ArtistListComponent } from "./artistList/artist_list.component";
import { LastMonthSongsComponent } from "./lastMonthSongs/last-month-songs.component";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    NavbarAppComponent,
    SearchBarComponent,
    SongsCarouselComponent,
    RouterModule,
    SearchBarComponent,
    SafeChoiceListComponent,
    TrendingSongsComponent,
    ArtistListComponent,
    LastMonthSongsComponent
],
  templateUrl: './dashboard.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DashboardComponent {}
