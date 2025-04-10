import { Routes } from '@angular/router';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { LandingComponent } from './features/landing/landing.component';
import { PlayerComponent } from './features/player/player.component';
import { LibraryComponent } from './features/library/library.component';
import { PlaylistComponent } from './features/playlist/playlist.component';
import { NotFoundComponent } from './features/404/404.component';
import { AboutUsComponent } from './features/landing/about/about.component';



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
        path: 'playlist/:id',
        component: PlaylistComponent,
    },
    {
        path: 'about-us',
        component: AboutUsComponent,
    },
    {
        path: '**',
        component: NotFoundComponent,
        data: { title: '404 - Not Found' }
    } // Esto previene rutas desconocidas

];
