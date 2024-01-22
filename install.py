import launch

if not launch.is_installed("jsonlines"):
    launch.run_pip("install jsonlines", "requirements for ArtJiggler")