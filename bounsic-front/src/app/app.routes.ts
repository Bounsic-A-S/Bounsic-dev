import { Routes } from '@angular/router';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { LandingComponent } from './features/landing/landing.component';
import { PlayerComponent } from './features/player/player.component';
import { LibraryComponent } from './features/library/library.component';
import { PlaylistComponent } from './features/playlist/playlist.component';

export const routes: Routes = [
    {
        path: '',
        component: LandingComponent,
    },
    {
        path: 'dashboard',
        component: DashboardComponent,
    },
    {
        path: 'player',
        component: PlayerComponent,
    },
    {
        path: 'library',
        component: LibraryComponent,
    },
    {
        path: 'playlist',
        component: PlaylistComponent,
    },
    { path: '**', redirectTo: '' } // Esto previene rutas desconocidas

];
