# rename_photo_based_on_taken_dates
Merge multiple photo folders into one, sort/rename photos based on taken dates.

Yes! The idea is simple. On a trip, many people usually take photos of not only themselves (selfie) but also the whole group. At the end, we all upload our photos to the same place, e.g. Google Drive, but in different folders. Different cameras have different photo numbering as well as some other photos are already there in the camera beforehand, making it impossible to get back to your trip chronologically . It, thus, comes to the need that after collecting all of them into one big folder, name them based on Date Taken property.

# Usage

```python
python.exe rename_photo_based_on_taken_dates.py -i "Input Directory" -o "Output Directory"
```

# Notes
3rd party library `PIL` is needed. (`pip install Pillow`)
