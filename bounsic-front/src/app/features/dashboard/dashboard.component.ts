import { ChangeDetectionStrategy, Component } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/components/navbar/navbar-app.component';
import { SearchBarComponent } from './searchBar/search-bar.component';
import { SongsCarouselComponent } from "./songsCarousel/songs-carousel.component";
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [NavbarAppComponent, SearchBarComponent, SongsCarouselComponent, RouterModule],
  templateUrl: './dashboard.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DashboardComponent { }
