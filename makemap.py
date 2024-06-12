import os
import face_recognition
import folium
import base64

known_image = face_recognition.load_image_file("test.jpg")   
known_face_encoding = face_recognition.face_encodings(known_image)[0]

def recognize_faces_in_frames(frames_dir, known_face_encoding):
    for frame_file in os.listdir(frames_dir):
        frame_path = os.path.join(frames_dir, frame_file)
        frame_image = face_recognition.load_image_file(frame_path)
        face_encodings = face_recognition.face_encodings(frame_image)

        for face_encoding in face_encodings:
            match = face_recognition.compare_faces([known_face_encoding], face_encoding)
            if match[0]:
                return frame_path   
    return None

 
video_locations = {
    'bloger.mp4': [48.8584, 2.2945],  
    'my_heart.mp4': [41.8781, -87.6298],
    'norm.mp4': [40.7580, -73.9855],
    'test.mp4': [48.8584, 2.2945],
    'john.mp4': [40.7128, -74.0060],
}

 
frames_dirs = [
    'frames_bloger.mp4',
    'frames_my_heart.mp4',
    'frames_norm.mp4',
    'frames_test.mp4',
    'frames_john.mp4'
]

 
matched_frames = []
for frames_dir in frames_dirs:
    video_name = "_".join(frames_dir.split('_')[1:])   
    matched_frame = recognize_faces_in_frames(frames_dir, known_face_encoding)
    if matched_frame:
        matched_frames.append((matched_frame, video_name))
        print(f"Match found in video: {video_name}, frame: {matched_frame}")

 
map_center = [48.8584, 2.2945]   
map = folium.Map(location=map_center, zoom_start=2)

 
def add_image_to_map(image_path, location, map_object, popup_text):
    encoded = base64.b64encode(open(image_path, 'rb').read()).decode()
    html = f'<img src="data:image/png;base64,{encoded}" width="300" height="200">'
    iframe = folium.IFrame(html, width=320, height=220)
    popup = folium.Popup(iframe, max_width=320)
    folium.Marker(location=location, popup=popup, tooltip=popup_text).add_to(map_object)

 
for matched_frame, video_name in matched_frames:
    location = video_locations[video_name]
    add_image_to_map(matched_frame, location, map, f"Matched Frame from {video_name}")

 
map_path = 'map.html'
map.save(map_path)

print(f"Map saved to {map_path}")
