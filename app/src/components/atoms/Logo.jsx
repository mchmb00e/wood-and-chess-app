function Logo({ image, width, height, alt }) {

    return (
        <div>
            <img src={image} alt={alt} height={height} width={width} />
        </div>
    );

}

export default Logo;