import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { ArtistListItemComponent } from './artist_item/artist_item.component';
@Component({
    selector: 'dashboard-artist-list',
    standalone: true,
    imports: [CommonModule,ArtistListItemComponent],
    templateUrl: './artist_list.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ArtistListComponent {

    public featuredArtists = [
        {
            id: 1,
            name: 'Coldplay',
            image: 'https://i.pinimg.com/736x/9a/5d/ec/9a5dec457d79fb2916fda52c6f831652.jpg',
            albums: ['Parachutes', 'A Rush of Blood to the Head', 'X&Y'],
        },
        {
            id: 2,
            name: 'Radiohead',
            image: 'https://i.pinimg.com/736x/4c/b9/78/4cb9781154d0dd1a316d5b45124f0912.jpg',
            albums: ['Pablo Honey', 'OK Computer', 'In Rainbows'],
        },
        {
            id: 3,
            name: 'Green Day',
            image: 'https://i.pinimg.com/736x/ae/b9/70/aeb970e9c064d436bda11462fc889489.jpg',
            albums: ['American Idiot', 'Dookie', '21st Century Breakdown'],
        },
        {
            id: 4,
            name: 'Hozier',
            image: 'https://i.pinimg.com/736x/a6/47/91/a64791f712cb10397610c83aa2612895.jpg',
            albums: ['Hozier', 'Wasteland, Baby!', 'Unreal Unearth'],
        },
        {
            id: 5,
            name: 'Imagine Dragons',
            image: 'https://i.pinimg.com/736x/5b/4c/ed/5b4ced22923bd1c1353d28213bffad03.jpg',
            albums: ['Evolve', 'Night Visions', 'Mercury – Acts 1 & 2'],
        },
        {
            id: 6,
            name: 'Mark Ronson ft. Bruno Mars',
            image: 'https://i.pinimg.com/736x/6c/f6/7f/6cf67f7ed6227a20b15035bd57d8927f.jpg',
            albums: ['Uptown Special', 'Version', 'Late Night Feelings'],
        },
        {
            id: 7,
            name: 'Red Hot Chili Peppers',
            image: 'https://i.pinimg.com/736x/c7/dc/60/c7dc60cfeaab1c085d3bba491826a06b.jpg',
            albums: ['By the Way', 'Californication', 'Stadium Arcadium'],
        }
    ];

}
