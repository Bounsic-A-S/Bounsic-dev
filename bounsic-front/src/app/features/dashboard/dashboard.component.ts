import { ChangeDetectionStrategy, Component } from '@angular/core';
import { NavbarAppComponent } from '@app/shared/components/navbar/navbar-app.component';
import { SearchBarComponent } from './searchBar/searchBar.component';
import { SongsCarouselComponent } from "./songsCarousel/songsCarousel.components";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [NavbarAppComponent, SearchBarComponent, SongsCarouselComponent],
  templateUrl: './dashboard.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DashboardComponent {}
