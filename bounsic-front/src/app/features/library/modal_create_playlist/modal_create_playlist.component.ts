import {
  ChangeDetectionStrategy,
  Component,
  EventEmitter,
  Input,
  Output,
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
import { AuthService } from '@app/services/auth/auth.service';
import { PlaylistService } from '@app/services/playlist.service';

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
  @Input() isOpen = false;
  @Output() closeModal = new EventEmitter<void>();

  isSubmitting = false;
  registerForm: FormGroup;
  Pencil = Pencil;
  previewImg: string | null = null;
  selectedImageFile: File | null = null;

  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private playlistService = inject(PlaylistService);

  constructor() {
    this.registerForm = this.fb.group({
      playlist_title: ['', [Validators.required]],
    });
  }

  close(): void {
    this.closeModal.emit();
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
    this.isSubmitting = true;

    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      this.isSubmitting = false;
      return;
    }

    const user = this.authService.getUserProfile();
    if (!user?.id_user) {
      console.error('El usuario no está autenticado');
      this.isSubmitting = false;
      return;
    }

    const playlist_title = this.registerForm.get('playlist_title')?.value;

    const formData = new FormData();
    formData.append('playlist_name', playlist_title);
    formData.append('user_id', user.id_user.toString());

    if (this.selectedImageFile) {
      formData.append('img_url', this.selectedImageFile);
    }

    console.log('Formulario válido. Enviando datos...');

    this.playlistService.createPlaylist(formData).subscribe((success) => {
      if (success) {
        console.log('Playlist creada exitosamente');
      } else {
        console.log('Error al crear playlist');
      }
    });
  }
}
