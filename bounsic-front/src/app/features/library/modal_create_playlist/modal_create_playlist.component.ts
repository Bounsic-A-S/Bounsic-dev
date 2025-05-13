import {
  ChangeDetectionStrategy,
  Component,
  Input,
  inject,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { ClickOutsideDirective } from '@app/directive/clickoutside.directive';
import { TranslateModule } from '@ngx-translate/core';
import { LucideAngularModule, Pencil } from 'lucide-angular';

@Component({
  selector: 'playlist-modal-create',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    ClickOutsideDirective,
    TranslateModule,
    LucideAngularModule,
  ],
  templateUrl: './modal_create_playlist.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ModalCreatePlaylistComponent {
  @Input() isOpen = true;

  isSubmitting = false;
  registerForm: FormGroup;
  Pencil = Pencil;
  previewImg: string | null = null;
  selectedImageFile: File | null = null;

  private fb = inject(FormBuilder);

  constructor() {
    this.registerForm = this.fb.group({
      playlist_title: ['', [Validators.required]],
    });
  }

  close(): void {
    this.isOpen = false;
  }
  onImageChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files?.[0]) {
      const file = input.files[0];
      this.selectedImageFile = file;
      this.previewImg = URL.createObjectURL(file);
    }
  }
  onSubmit(): void {
    const formValues = this.registerForm.value;
    if(!formValues) return 
    const playlist_title = formValues.playlist_title
    console.log(playlist_title)
    const formData = new FormData()
    formData.append('title', playlist_title)
    if (this.selectedImageFile) {
      formData.append('profile_img', this.selectedImageFile);
    }
  }
}
