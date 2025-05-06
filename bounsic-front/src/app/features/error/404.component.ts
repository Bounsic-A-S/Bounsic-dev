import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { Router } from '@angular/router';
import { NotFoundButtonComponent } from './button/404_button.component';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import data from './data.json';

@Component({
  selector: 'app-router-err',
  standalone: true,
  templateUrl: './404.component.html',
  styleUrl: './404.component.css',
  imports: [CommonModule, NotFoundButtonComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  schemas: [CUSTOM_ELEMENTS_SCHEMA] // for web components function props

})
export class NotFoundComponent {
  constructor(private readonly router: Router) { }
  public phrase : Phrase= {
    "phrase": "does not exist",
    "song": "does not exist",
    "artist": "does not exist"
  }
  public content404: Phrase[] = data as Phrase[];


  redirectToDashboard = (): void => {
    this.router.navigate(['/']);
  }

  chose_phrase = (): Phrase => {
    const index = Math.floor(Math.random() * this.content404.length);
    this.phrase= this.content404[index];
    return this.phrase
  }
  

  
  
}


interface Phrase {
  phrase: string;
  song: string;
  artist: string;
}

