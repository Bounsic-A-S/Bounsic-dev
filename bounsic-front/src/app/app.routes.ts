import { Routes } from '@angular/router';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { LandingComponent } from './features/landing/landing.component';
import { PlayerComponent } from './features/player/player.component';
import { LibraryComponent } from './features/library/library.component';
import { PlaylistComponent } from './features/playlist/playlist.component';
import { NotFoundComponent } from './features/404/404.component';
import { SettingsComponent } from './features/user/settings/setting.component';
import { SettingsAccountComponent } from './features/user/settings/account/account.component';
import { SettingsAppearanceComponent } from './features/user/settings/color/appearance.component';
import { AboutUsComponent } from './features/landing/about/about.component';
import { LanguageComponent } from './features/user/settings/i18n/language.component';


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
        path:'settings',
        component: SettingsComponent,
        children: [
            { path: '', redirectTo: 'account', pathMatch: 'full' },
            { path: 'account', component: SettingsAccountComponent },
            // { path: 'privacy', component: PrivacyComponent },
            // { path: 'connections', component: ConnectionsComponent },
            // { path: 'notifications', component: NotificationsComponent },
            // { path: 'plan', component: PlanComponent },
            // { path: 'playback', component: PlaybackComponent },
            { path: 'appearance', component: SettingsAppearanceComponent },
            { path: 'language', component: LanguageComponent }
          ]
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
