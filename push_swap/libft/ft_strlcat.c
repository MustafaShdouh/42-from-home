/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/10 15:10:10 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/10 15:42:21 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
//#include <string.h>
//#include <stddef.h>
#include "libft.h"

size_t	ft_strlcat(char *dst, const char *src, size_t size)
{
	size_t	srclen;
	size_t	dstlen;
	size_t	i;

	i = 0;
	if ((!dst || !src) && size == 0)
		return (0);
	srclen = ft_strlen(src);
	dstlen = 0;
	while (dst[dstlen] && dstlen < size)
		dstlen++;
	if (dstlen == size)
		return (size + srclen);
	while (src[i] && (dstlen + i + 1) < size)
	{
		dst[dstlen + i] = src[i];
		i++;
	}
	dst[dstlen + i] = '\0';
	return (dstlen + srclen);
}

/*int main()
{
    char first[] = "This is ";
    char last[] = "a potentially long string";
    int r;
    int size = 16;
    char buffer[size];

    strcpy(buffer,first);
    r = ft_strlcat(buffer,last,size);

    printf("%s\n", buffer);
    printf("Value returned: %d\n",r);
    if(r > size)
        printf("String truncated\n");
    else
        printf("String was fully copied\n");

    return(0);
}*/
